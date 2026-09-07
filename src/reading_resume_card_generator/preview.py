from __future__ import annotations

import json
from typing import Any


def render_html(report: dict[str, Any]) -> str:
    payload = json.dumps(report).replace("<", "\\u003c").replace("&", "\\u0026")
    return (
        """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reading checkpoint card</title><style>body{font:17px system-ui;background:#f4f1e9;color:#203742;max-width:700px;margin:auto;padding:22px}
article{background:white;border:1px solid #aebfc6;border-radius:12px;padding:22px}label{display:block;margin:12px 0}
input,select{font:inherit;padding:8px;max-width:100%;box-sizing:border-box}li{margin:9px 0}
@media print{.controls{display:none}body{padding:0;background:white}article{border:0;max-width:95mm;font-size:11pt;break-inside:avoid}}
</style><h1>Reading checkpoint card</h1><div class="controls">
<p>This export contains only facts up to its ceiling. To advance beyond it, regenerate from your private source.</p>
<label>Checkpoint <input id="checkpoint" type="number" min="0"></label>
<label>Layout <select id="layout"><option value="phone">Phone</option><option value="pocket">Pocket print</option></select></label>
</div><article id="card"></article><p id="status" role="status"></p>
<script type="application/json" id="data">"""
        + payload
        + """</script><script>
const data=JSON.parse(document.getElementById('data').textContent);const checkpoint=document.getElementById('checkpoint');
checkpoint.max=data.through;checkpoint.value=data.through;
function draw(){const through=Math.min(data.through,Math.max(0,Math.floor(Number(checkpoint.value)||0)));
const card=document.getElementById('card');card.replaceChildren();const title=document.createElement('h2');title.textContent=data.work;card.append(title);
const summary=document.createElement('p');summary.textContent=`Checkpoint ${through} · ${data.next_step}`;card.append(summary);
let newly=0,hidden=Object.values(data.still_hidden).reduce((a,b)=>a+b,0);
for(const [label,items] of [['Events',data.visible_events],['Characters',data.characters],['Threads',[...data.open_threads,...data.resolved_threads]]]){
 const h=document.createElement('h3');h.textContent=label;card.append(h);const ul=document.createElement('ul');
 for(const item of items){if(item.milestone>through){hidden++;continue;}const li=document.createElement('li');
 const fresh=item.milestone>data.previous_checkpoint;if(fresh)newly++;
 li.textContent=`${fresh?'New: ':''}${item.text??item.name} · milestone ${item.milestone}`;ul.append(li);}card.append(ul);
}document.getElementById('status').textContent=`${newly} facts since the previous checkpoint; ${hidden} items remain hidden. Export ceiling ${data.through}.`;
card.style.maxWidth=document.getElementById('layout').value==='pocket'?'95mm':'100%';}
checkpoint.addEventListener('input',draw);document.getElementById('layout').addEventListener('change',draw);draw();</script></html>"""
    )
