'use strict';
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const scenes = $$('.scene');
const dialog = $('#detail');
const stage = $('#stage');
let current = 0, returnFocus = null, methodStep = 0, powerStep = 0;
const external = (url,label) => `<a class="external" href="${url}" target="_blank" rel="noopener noreferrer">${label} · online ↗</a>`;
function pressed(selector, index) {
  $$(selector).forEach((el,i)=>el.setAttribute('aria-pressed',String(i===index)));
}
function resize() {
  const viewport = $('#viewport');
  stage.style.setProperty('--scale', Math.min(viewport.clientWidth/1600,viewport.clientHeight/900));
}
function go(index, focusHeading=false) {
  const previousFocusScene=document.activeElement.closest('.scene');
  const previousIndex = current;
  current = Math.max(0,Math.min(scenes.length-1,index));
  focusHeading ||= !!previousFocusScene && previousFocusScene!==scenes[current];
  scenes.forEach((s,i)=>{s.hidden=i!==current;s.classList.toggle('active',i===current);s.inert=i!==current;});
  $('#counter').textContent=`${String(current+1).padStart(2,'0')} / 08`;
  $('#scene-name').textContent=titles[current];
  $('#prev').disabled=current===0;$('#next').disabled=current===7;
  if(location.hash!==`#${current+1}`) history.replaceState(null,'',`#${current+1}`);
  $('#announcement').textContent=`${copy.announce(current+1)} ${titles[current]}`;
  const alternate = $('#alternate-language');
  alternate.hash = location.hash;
  if (previousIndex !== current) $('#viewport').scrollTop = 0;
  if(focusHeading){const h=scenes[current].querySelector('h1,h2');h.tabIndex=-1;h.focus({preventScroll:true});}
  else if(document.activeElement.disabled) $('#scene-menu').focus({preventScroll:true});
}
function openDialog(title, body, kicker=copy.detail) {
  returnFocus=document.activeElement;
  $('#dialog-title').textContent=title;$('#dialog-kicker').textContent=kicker;
  $('#dialog-body').innerHTML=body;
  dialog.showModal();dialog.scrollTop=0;$('#close-dialog').focus();
}
function closeDialog(){dialog.close();}
dialog.addEventListener('close',()=>{if(returnFocus?.isConnected&&!returnFocus.closest('[hidden]')) returnFocus.focus({preventScroll:true});});
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)closeDialog();}});
$('#close-dialog').onclick=closeDialog;
dialog.addEventListener('keydown', event => {
 if (event.key !== 'Tab') return;
 const items = [...dialog.querySelectorAll('a[href], button:not(:disabled)')].filter(el => !el.closest('[hidden]'));
 const edge = event.shiftKey ? items[0] : items.at(-1);
 if (document.activeElement === edge) {
  event.preventDefault();
  (event.shiftKey ? items.at(-1) : items[0]).focus();
 }
});
function showDetail(type) {
 const [title, body, kicker] = details[type];
 openDialog(title, body(), kicker);
}
function evidence(){
 if(current===2)return showDetail('essay');
 if([3,5,7].includes(current))return showDetail('privacy');
 if(current===4)return showDetail('triad');
 if(current===6)return showDetail('law');
 openDialog(...introduction);
}
function updateMethod(n){
 methodStep=n;pressed('[data-method]',n);const [name,q,desc,out]=method[n];
 $('#method-insight').innerHTML=`<span class="step-count">0${n+1} / 06</span><h3>${name}</h3><p class="method-question">${q}</p><p>${desc}</p><div class="method-deliverable"><span>${copy.makeExplicit}</span><b>${out}</b></div>`;
}
function updatePower(n){
 powerStep=n;pressed('[data-power]',n);$('#scena-7').dataset.state=n;
 $('#power-insight').innerHTML = powerBodies[n];
}
function showHelp(){openDialog(...help);}
async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else if(document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else throw new Error('unsupported');}catch{openDialog(...fullscreenFallback);}}
$('#prev').onclick=()=>go(current-1);$('#next').onclick=()=>go(current+1);$('#evidence').onclick=evidence;$('#fullscreen').onclick=fullscreen;$('#help').onclick=showHelp;
$('#static').onclick=()=>{const on=document.body.classList.toggle('static');$('#static').setAttribute('aria-pressed',on);$('#announcement').textContent=on?copy.animationsOff:copy.animationsOn;};
$('#scene-menu').onclick=()=>openDialog(copy.index,`<ol class="scene-index">${titles.map((t,i)=>`<li><button data-go="${i}">${String(i+1).padStart(2,'0')} · ${t}</button></li>`).join('')}</ol>`,copy.indexKicker);
document.addEventListener('click',event=>{
 const el=event.target.closest('button');if(!el)return;
 if(el.hasAttribute('data-dialog'))showDetail(el.dataset.dialog);
 if(el.hasAttribute('data-question')){const n=+el.dataset.question;pressed('[data-question]',n);const [label,title,body]=questions[n];$('#question-insight').innerHTML=`<span class="mini">0${n+1} · ${label}</span><h3>${title}</h3><p>${body}</p>`;}
 if(el.hasAttribute('data-story')){const n=+el.dataset.story;pressed('[data-story]',n);$('#story-insight').innerHTML=story[n];}
 if(el.hasAttribute('data-editorial')){const n=+el.dataset.editorial;pressed('[data-editorial]',n);$('#editorial-insight').textContent=editorial[n];}
 if(el.hasAttribute('data-principle')){const n=+el.dataset.principle;pressed('[data-principle]',n);$('#principle-insight').innerHTML=`<b>${principles[n][0]}</b><p>${principles[n][1]}</p>`;}
 if(el.hasAttribute('data-method'))updateMethod(+el.dataset.method);
 if(el.hasAttribute('data-method-next'))updateMethod((methodStep+1)%6);
 if(el.hasAttribute('data-power'))updatePower(+el.dataset.power);
 if(el.hasAttribute('data-power-next')){updatePower(Math.min(2,powerStep+1));const next=$('#power-insight button');next?.focus();}
 if(el.hasAttribute('data-decision')){const correct=el.dataset.decision==='correct';pressed('[data-decision]',correct?0:1);$('.decision-feedback').textContent=correct?copy.corrected:copy.rejected;}
 if(el.hasAttribute('data-language') && el.closest('.triad-switch')){const lang=el.dataset.language;$$('[data-language]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.language===lang));$$('[data-language-panel]').forEach(p=>p.hidden=p.dataset.languagePanel!==lang);}
 if(el.hasAttribute('data-go')){returnFocus=null;closeDialog();go(+el.dataset.go,true);}
});
document.addEventListener('keydown',e=>{
 if(e.ctrlKey||e.metaKey||e.altKey||e.isComposing)return;
 if(dialog.open){if(e.key==='Escape'){e.preventDefault();closeDialog();}return;}
 if(e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
 const k=e.key.toLowerCase();
 if(['arrowright','pagedown','arrowleft','pageup','home','end'].includes(k)){e.preventDefault();go(k==='home'?0:k==='end'?7:current+(['arrowright','pagedown'].includes(k)?1:-1));}
 else if(k===' '&&!e.target.closest('button,a')){e.preventDefault();go(current+1);}
 else if(k==='e'){e.preventDefault();evidence();}else if(k==='f'){e.preventDefault();fullscreen();}else if(k==='s'){e.preventDefault();$('#static').click();}else if(k==='?')showHelp();
});
window.addEventListener('hashchange',()=>{const n=Number(location.hash.slice(1));if(Number.isInteger(n)&&n>=1&&n<=8){if(dialog.open)closeDialog();go(n-1);}});
window.addEventListener('resize',resize);
document.addEventListener('fullscreenchange',()=>{$('#fullscreen').setAttribute('aria-pressed',!!document.fullscreenElement);resize();});
resize();const initial=Number(location.hash.slice(1));go(Number.isInteger(initial)&&initial>=1&&initial<=8?initial-1:0);
