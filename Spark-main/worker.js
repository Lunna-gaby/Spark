const statuses = ['Ativa','Em andamento','Devolvida','Cancelada'];
const json = (body,status=200) => Response.json(body,{status,headers:{'Cache-Control':'no-store'}});
const fail = (erro,status=400) => json({erro},status);
async function authorized(request,env) {
  if (!env.ADMIN_PASSWORD) return false;
  let credentials;
  try { credentials=atob((request.headers.get('Authorization')||'').replace(/^Basic /,'')); } catch { return false; }
  const digest=async v=>new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(v)));
  const [a,b]=await Promise.all([digest(credentials),digest(`admin:${env.ADMIN_PASSWORD}`)]);
  let diff=0; for(let i=0;i<a.length;i++) diff|=a[i]^b[i]; return diff===0;
}
export default {async fetch(request,env) {
  const url=new URL(request.url),path=url.pathname.replace(/\/$/,'')||'/',method=request.method;
  const match=path.match(/^\/reservas\/([1-9]\d*)(\/status)?$/);
  const privateRoute=['/reservas-realizadas','/reservas-realizadas.html','/api/reservas'].includes(path)||Boolean(match);
  if(privateRoute&&!await authorized(request,env)) {
    if(!env.ADMIN_PASSWORD) return fail('Configure a senha da administração antes de acessar.',503);
    return new Response('Acesso restrito à direção. Usuário: admin.',{status:401,headers:{'WWW-Authenticate':'Basic realm="Direcao ReservaEdu", charset="UTF-8"','Cache-Control':'no-store'}});
  }
  if(['POST','PUT','DELETE'].includes(method)&&request.headers.get('Origin')&&request.headers.get('Origin')!==url.origin) return fail('Origem não permitida.',403);
  try {
    if(method==='GET'&&['/','/reservas','/reservas-realizadas'].includes(path)) {
      const asset={'/':'/index.html','/reservas':'/reservas.html','/reservas-realizadas':'/reservas-realizadas.html'}[path];
      const response=await env.ASSETS.fetch(new Request(new URL(asset,url),request));
      const headers=new Headers(response.headers);headers.set('X-Content-Type-Options','nosniff');
      if(privateRoute)headers.set('Cache-Control','no-store');
      return new Response(response.body,{status:response.status,headers});
    }
    if(method==='GET'&&path==='/equipamentos') return json((await env.DB.prepare('SELECT id,nome,descricao,quantidade FROM equipamentos ORDER BY id').all()).results);
    if(method==='GET'&&path==='/api/reservas') return json((await env.DB.prepare('SELECT * FROM reservas ORDER BY id DESC').all()).results);
    if(method==='POST'&&path==='/reservas') {
      if(!request.headers.get('Content-Type')?.includes('application/json'))return fail('Envie os dados em JSON.',415);
      if(Number(request.headers.get('Content-Length')||0)>8192)return fail('Dados muito grandes.',413);
      const text=await request.text();if(text.length>8192)return fail('Dados muito grandes.',413);
      let body;try{body=JSON.parse(text)}catch{return fail('JSON inválido.')}
      const fields=['nome_aluno','matricula','equipamento','data','hora_retirada','hora_devolucao'];
      if(!body||fields.some(f=>typeof body[f]!=='string'||!body[f].trim()||body[f].length>200))return fail('Preencha todos os campos corretamente.');
      const [nome,matricula,equipamento,data,retirada,devolucao]=fields.map(f=>body[f].trim());
      if(!/^\d{4}-\d{2}-\d{2}$/.test(data)||!Number.isFinite(Date.parse(data+'T00:00:00Z'))||new Date(data+'T00:00:00Z').toISOString().slice(0,10)!==data)return fail('Data inválida.');
      if(![retirada,devolucao].every(h=>/^([01]\d|2[0-3]):[0-5]\d$/.test(h))||retirada>=devolucao)return fail('A devolução precisa ser após a retirada, no mesmo dia.');
      const item=await env.DB.prepare('SELECT id FROM equipamentos WHERE nome = ?').bind(equipamento).first();
      if(!item)return fail('Equipamento não encontrado.',404);
      const result=await env.DB.prepare(`INSERT INTO reservas(nome_aluno,matricula,equipamento,data,hora_retirada,hora_devolucao,status)
        SELECT ?,?,?,?,?,?,'Ativa' FROM equipamentos e WHERE e.id=? AND e.quantidade>
        (SELECT COUNT(*) FROM reservas r WHERE r.equipamento=e.nome AND r.data=? AND r.status IN ('Ativa','Em andamento') AND r.hora_retirada<? AND r.hora_devolucao>?)`)
        .bind(nome,matricula,equipamento,data,retirada,devolucao,item.id,data,devolucao,retirada).run();
      if(!result.meta.changes)return fail('Não há unidade disponível nesse horário.',409);
      return json({mensagem:'Reserva realizada com sucesso!',reserva:{id:result.meta.last_row_id,nome_aluno:nome,matricula,equipamento,data,hora_retirada:retirada,hora_devolucao:devolucao,status:'Ativa'}},201);
    }
    if(match&&['PUT','DELETE'].includes(method)) {
      const id=Number(match[1]);
      if(!await env.DB.prepare('SELECT id FROM reservas WHERE id=?').bind(id).first())return fail('Reserva não encontrada.',404);
      if(method==='DELETE'&&!match[2]){await env.DB.prepare('DELETE FROM reservas WHERE id=?').bind(id).run();return json({mensagem:'Reserva excluída com sucesso!'})}
      if(method==='PUT'&&match[2]) {
        const status=url.searchParams.get('status');if(!statuses.includes(status))return fail('Status inválido.');
        const result=await env.DB.prepare(`UPDATE reservas SET status=? WHERE id=? AND
          (? NOT IN ('Ativa','Em andamento') OR
          (SELECT quantidade FROM equipamentos WHERE nome=reservas.equipamento)>
          (SELECT COUNT(*) FROM reservas r WHERE r.id!=reservas.id AND r.equipamento=reservas.equipamento AND r.data=reservas.data AND r.status IN ('Ativa','Em andamento') AND r.hora_retirada<reservas.hora_devolucao AND r.hora_devolucao>reservas.hora_retirada))`).bind(status,id,status).run();
        if(!result.meta.changes)return fail('Não há unidade disponível para reativar essa reserva.',409);
        return json({mensagem:'Status alterado com sucesso!',status});
      }
    }
    if(method==='GET')return env.ASSETS.fetch(request);
    return fail('Rota não encontrada.',404);
  }catch(error){console.error(error.message);return fail('Erro interno. Verifique o banco D1 e as migrações.',500)}
}};
