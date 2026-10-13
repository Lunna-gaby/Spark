import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import {Script} from 'node:vm';
import worker from '../worker.js';
function setup(){
 const db=new DatabaseSync(':memory:');db.exec(readFileSync(new URL('../migrations/0001_schema.sql',import.meta.url),'utf8'));
 return {ADMIN_PASSWORD:'test-only',ASSETS:{fetch:async req=>new Response(readFileSync(new URL('../public'+new URL(req.url).pathname,import.meta.url),'utf8'))},DB:{prepare(sql){let values=[];return {bind(...args){values=args;return this},async all(){return {results:db.prepare(sql).all(...values)}},async first(){return db.prepare(sql).get(...values)||null},async run(){const r=db.prepare(sql).run(...values);return {meta:{changes:Number(r.changes),last_row_id:Number(r.lastInsertRowid)}}}}}}};
}
const auth={Authorization:'Basic '+btoa('admin:test-only')};
const reservation={nome_aluno:'Aluno teste',matricula:'123',equipamento:'Projetor',data:'2026-10-13',hora_retirada:'08:00',hora_devolucao:'09:00'};
const call=(env,path,method='GET',body,headers={})=>worker.fetch(new Request('https://example.test'+path,{method,headers:{...(body?{'Content-Type':'application/json'}:{}),...headers},...(body?{body:JSON.stringify(body)}:{})}),env);
test('telas e JavaScript do navegador são válidos',async()=>{
 const env=setup();for(const [route,file] of [['/','index.html'],['/reservas','reservas.html'],['/reservas-realizadas','reservas-realizadas.html']]){
  assert.equal((await call(env,route,'GET',null,auth)).status,200);
  const html=readFileSync(new URL('../public/'+file,import.meta.url),'utf8');
  for(const m of html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g))new Script(m[1]);
 }
});
test('listagem, criação, capacidade, cancelamento, reativação e exclusão',async()=>{
 const env=setup();assert.equal((await (await call(env,'/equipamentos')).json()).length,4);
 const first=await call(env,'/reservas','POST',reservation);assert.equal(first.status,201);
 const id=(await first.json()).reserva.id;
 assert.equal((await call(env,'/reservas','POST',reservation)).status,201);
 assert.equal((await call(env,'/reservas','POST',reservation)).status,409);
 assert.equal((await call(env,`/reservas/${id}/status?status=Cancelada`,'PUT',null,auth)).status,200);
 assert.equal((await call(env,'/reservas','POST',reservation)).status,201);
 assert.equal((await call(env,`/reservas/${id}/status?status=Ativa`,'PUT',null,auth)).status,409);
 assert.equal((await call(env,'/reservas','POST',{...reservation,hora_retirada:'09:00',hora_devolucao:'10:00'})).status,201);
 assert.equal((await (await call(env,'/api/reservas','GET',null,auth)).json()).length,4);
 assert.equal((await call(env,`/reservas/${id}`,'DELETE',null,auth)).status,200);
 assert.equal((await call(env,`/reservas/${id}`,'DELETE',null,auth)).status,404);
});
test('proteção da direção, entradas inválidas e origens',async()=>{
 const env=setup();for(const path of ['/reservas-realizadas','/reservas-realizadas.html','/api/reservas','/reservas/1'])assert.equal((await call(env,path)).status,401);
 assert.equal((await call({...env,ADMIN_PASSWORD:''},'/api/reservas')).status,503);
 assert.equal((await call(env,'/api/reservas','GET',null,{Authorization:'Basic '+btoa('admin:wrong')})).status,401);
 for(const body of [{...reservation,data:'2026-02-30'},{...reservation,hora_devolucao:'07:00'},{...reservation,nome_aluno:''}])assert.equal((await call(env,'/reservas','POST',body)).status,400);
 assert.equal((await call(env,'/reservas','POST',{...reservation,equipamento:'Inexistente'})).status,404);
 assert.equal((await call(env,'/reservas','POST',reservation,{Origin:'https://other.test'})).status,403);
});
