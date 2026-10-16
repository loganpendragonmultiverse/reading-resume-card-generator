// Exercise the exported preview script with a minimal DOM and no browser network.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const html = fs.readFileSync(process.argv[2], 'utf8');
const elements = new Map();
function element() { return {textContent:'',value:'',style:{},children:[],
  append(child){this.children.push(child)},replaceChildren(){this.children=[]},
  addEventListener(){}}; }
global.document={createElement:element,getElementById(id){if(!elements.has(id))elements.set(id,element());return elements.get(id)}};
document.getElementById('data').textContent=html.match(/id="data">([\s\S]*?)<\/script>/)[1];
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const vm=require('node:vm');
vm.runInThisContext(code);
const checkpoint=document.getElementById('checkpoint');
function text(node){return node.textContent+' '+node.children.map(text).join(' ')}
for(const [point,status] of [[4,'open'],[5,'resolved'],[6,'resolved']]){
 checkpoint.value=point;vm.runInThisContext('draw()');
 assert.match(text(document.getElementById('card')),new RegExp('letter.*'+status));
}
checkpoint.value=100;vm.runInThisContext('draw()');
assert.match(text(document.getElementById('card')),/Checkpoint 6/);
checkpoint.value=4;vm.runInThisContext('draw()');
assert.doesNotMatch(text(document.getElementById('card')),/resolved/);
console.log('HTML preview boundaries and ceiling passed');
