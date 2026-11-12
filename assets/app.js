const activities = window.PORTFOLIO_ACTIVITIES || [];
const grid = document.querySelector('#activities');
const dialog = document.querySelector('#activity-dialog');
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fileURL = path => path.split('/').map(encodeURIComponent).join('/');
const paragraphs = text => String(text).split(/\n\n+/).map(p=>`<p>${escapeHTML(p)}</p>`).join('');
const symbols = {'01':'01','05':'05','09':'09','17':'17','02':'Aa','03':'✳','04':'ƒ(x)','06':'06','08':'{ }','10':'↗','11':'↗','12':'12','14':'[ ]','15':'≋','16':'↯','18':'✳'};
let previousFocus;
function render(term='All') {
 const shown = activities.filter(item => term==='All' || item.term===term);
 grid.innerHTML = shown.map(item => `<article class="activity" data-kind="${item.tags.includes('Exam')?'assessment':'work'}"><button class="activity-link" data-activity="${item.id}" aria-label="Explore ${escapeHTML(item.title)}"><div class="activity-visual" aria-hidden="true"><span class="visual-corner">${item.term.toUpperCase()} / ${item.week}</span><div class="visual-lines"></div><span class="visual-symbol">${symbols[item.week]||'✳'}</span><span class="visual-caption">${escapeHTML(item.topic.toUpperCase())}</span></div><div class="activity-body"><div class="activity-meta"><span>WEEK ${item.week}</span><span>${escapeHTML(item.tags[0])}</span></div><h3>${escapeHTML(item.title)}</h3><p class="activity-summary">${escapeHTML(item.summary)}</p><div class="activity-bottom"><span>${item.files.length?item.files.length+' artifact'+(item.files.length===1?'':'s'):(item.links?.length?'Portfolio entry':'Reflection')} · View activity</span><span class="activity-arrow" aria-hidden="true">↗</span></div></div></button></article>`).join('');
 document.querySelector('#work-count').textContent = `${shown.length} activities`;
 document.querySelector('.filters button[data-term="All"] span').textContent=activities.length;
 renderTakeaways(term);
}
function renderTakeaways(term) {
 const takeaways=window.PORTFOLIO_TAKEAWAYS||{};
 const terms=term==='All'?['Prelims','Midterms','Finals']:[term];
 document.querySelector('#term-takeaways').innerHTML=`<div class="takeaways-heading"><p class="eyebrow">LOOKING BACK</p><h3>Term takeaways</h3></div>${terms.map(name=>{const item=takeaways[name];if(!item)return '';return `<section class="term-takeaway" aria-labelledby="takeaway-${name.toLowerCase()}"><span class="takeaway-term">${name}</span><div><h4 id="takeaway-${name.toLowerCase()}">${escapeHTML(item.title)}</h4>${item.paragraphs.map(p=>`<p>${escapeHTML(p)}</p>`).join('')}<div class="takeaway-goals"><p><strong>My next step</strong>${escapeHTML(item.shortTerm)}</p><p><strong>Looking ahead</strong>${escapeHTML(item.longTerm)}</p></div></div></section>`}).join('')}`;
}
function renderEvidence(item) {
 const links=(item.links||[]).map(link=>`<a class="artifact evidence-reference" href="${escapeHTML(link.url)}" ${link.url.startsWith('#')?'data-local-section':'target="_blank" rel="noopener"'}><span class="file-info"><strong>${escapeHTML(link.label)}</strong></span><span aria-hidden="true">↗</span></a>`).join('');
 const missing=item.files.length||links?'':'<p class="evidence-missing">No supporting file has been uploaded for this activity yet.</p>';
 return `${missing}${links}${item.files.some(f=>f.type==='HEIC')?'<p class="heic-note">Original examination photos are available as HEIC downloads. A compatible image viewer may be required.</p>':''}<div class="artifact-list">${item.files.map(file=>renderArtifact(file,item)).join('')}</div>`;
}
function renderArtifact(file, item) {
 const size=file.size<1048576?Math.ceil(file.size/1024)+' KB':(file.size/1048576).toFixed(1)+' MB';
 if(file.type==='IPYNB') return `<div class="artifact"><span class="file-type">IPYNB</span><span class="file-info"><strong>${escapeHTML(file.name)}</strong><small>${size} · Code and saved results</small><span class="notebook-actions"><a class="view-notebook" href="notebooks/${item.id}.html" target="_blank" rel="noopener" aria-label="View notebook ${escapeHTML(file.name)}">View notebook ↗</a><a class="download-notebook" href="${fileURL(file.path)}" download aria-label="Download ${escapeHTML(file.name)}">Download .ipynb</a></span></span></div>`;
 const open=file.type==='PDF'||file.type==='PNG';
 return `<a class="artifact" href="${fileURL(file.path)}" ${open?'target="_blank" rel="noopener"':'download'} aria-label="${open?'Open':'Download'} ${escapeHTML(file.name)}"><span class="file-type">${file.type}</span><span class="file-info"><strong>${escapeHTML(file.name)}</strong><small>${size} · ${open?'Opens in a new tab':'Download original'}</small></span><span aria-hidden="true">↗</span></a>`;
}
function showActivity(id) {
 const item=activities.find(a=>a.id===id); if(!item)return;
 previousFocus=document.activeElement;
 document.querySelector('#dialog-label').textContent=`${item.term.toUpperCase()} / WEEK ${item.week}`;
 const assessment=item.tags.some(tag=>tag==='Quiz'||tag==='Exam');
 const hasPhotos=item.files.some(file=>['HEIC','HEIF','JPG','JPEG','PNG','WEBP'].includes(file.type));
 const evidence=(!assessment||hasPhotos)?`<section class="detail-section"><h3>The evidence</h3>${renderEvidence(item)}</section>`:'';
 const section=(title,content)=>content?`<section class="detail-section"><h3>${title}</h3>${paragraphs(content)}</section>`:'';
 document.querySelector('#activity-content').innerHTML=`<p class="eyebrow">WEEK ${item.week} · ${escapeHTML(item.term.toUpperCase())}</p><h2 id="activity-title">${escapeHTML(item.title)}</h2><p class="detail-summary">${escapeHTML(item.summary)}</p><div class="detail-tags">${item.tags.map(tag=>`<span>${escapeHTML(tag)}</span>`).join('')}</div>${evidence}${item.contributions?`<section class="detail-section contributions-section"><h3>My project contributions</h3>${item.contributions.map(c=>`<h4>${escapeHTML(c.title)}</h4><p>${escapeHTML(c.text)}</p>`).join('')}</section>`:''}${assessment?'':section('Skills learned',item.skills)+section('The “So What”',item.importance)}${section('Learning reflection',item.reflection)}${!item.reflection?'<p class="pending-note">Learning reflection in progress.</p>':''}<p class="detail-credit">${item.tags.includes('DecisionThree')||['11','14','15','16'].includes(item.week)?'DecisionThree · Group work':'Portfolio by Job Russel Enriquez'}</p>`;
 dialog.showModal();
}
document.querySelector('.filters').addEventListener('click',e=>{const button=e.target.closest('button[data-term]');if(!button)return;document.querySelectorAll('.filters button').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button))});render(button.dataset.term)});
grid.addEventListener('click',e=>{const button=e.target.closest('[data-activity]');if(button)showActivity(button.dataset.activity)});
document.querySelector('.close-button').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close()}});
dialog.addEventListener('click',e=>{if(e.target.closest('[data-local-section]'))dialog.close()});
dialog.addEventListener('close',()=>previousFocus?.focus());
render();
