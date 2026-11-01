/**
 * Mobbin WEB Screens Harvester — bookmarklet source (premium-web-design)
 * =====================================================================
 * Web-platform twin of the premium-mobile-design Mobbin harvester.
 *
 * Run it on a Mobbin WEB app page (https://mobbin.com/apps/<slug>-web).
 * It auto-scrolls, harvests full-res (unblurred) screenshots from the
 * bytescale.mobbin.com CDN via srcset, filters placeholders, zips them and
 * POSTs the archive to the local Web Ingestion Bridge:
 *
 *     POST http://127.0.0.1:3848/save?app=<slug>&category=<category>
 *
 * Files land in:
 *     premium-web-design/design-systems/<category>/<app>/screens/screen_001.webp ...
 *
 * If the bridge is not running, it falls back to a normal browser download of
 *     <app>__<category>__webscreens.zip
 * which the bridge's Downloads watcher picks up automatically on next start.
 *
 * Differences vs the mobile version:
 *   - Targets port 3848 (mobile bridge stays on 3847) — both can run at once.
 *   - Aspect filter adapted for web: keeps landscape viewport shots AND tall
 *     full-page captures; only rejects tiny icons and extreme phone-portrait
 *     shapes (the mobile one keeps portrait-only).
 *   - Fallback archive name uses the `__webscreens` marker so the mobile
 *     Downloads watcher never grabs it.
 *
 * Minify + URL-encode to produce the installable one-liner (see README_bridge.md).
 */

javascript:(async function(){
if(window.__mobbin_web_harvester_running){alert("⚠️ Mobbin WEB extraction is already in progress! Please wait for it to finish.");return;}
window.__mobbin_web_harvester_running=true;

var box=document.createElement('div');
box.style.cssText='position:fixed;top:20px;left:50%;transform:translateX(-50%);z-index:999999;background:#111827;color:#f9fafb;padding:16px 28px;border-radius:14px;font-family:sans-serif;font-size:14px;box-shadow:0 12px 30px rgba(0,0,0,0.6);border:1px solid #374151;text-align:center;min-width:340px;';

function cleanup(){window.__mobbin_web_harvester_running=false;setTimeout(function(){if(box&&box.parentElement)box.remove();},5000);}

function getAppSlug(){
  var m=location.pathname.match(/\/apps\/([^\/?#]+)/i);
  if(m&&m[1]){
    var s=m[1].replace(/-(ios|android|web).*$/i,'').replace(/-[0-9a-f]{8,}.*$/i,'');
    if(s&&!/^(apps?|browse|ios|android|web|loading|overview)$/i.test(s))return s;
  }
  try{
    var nData=window.__NEXT_DATA__&&window.__NEXT_DATA__.props&&window.__NEXT_DATA__.props.pageProps;
    var nApp=nData&&(nData.app||(nData.data&&nData.data.app));
    if(nApp&&nApp.name)return nApp.name;
  }catch(e){}
  try{
    var lds=document.querySelectorAll('script[type="application/ld+json"]');
    for(var i=0;i<lds.length;i++){
      var j=JSON.parse(lds[i].textContent||'{}');
      if(j.name&&!/mobbin/i.test(j.name))return j.name;
    }
  }catch(e){}
  var h1=document.querySelector('h1')&&document.querySelector('h1').textContent.trim();
  if(h1&&!/^(loading|apps?|browse|ios|android|web|screens|ui\s*patterns|overview)$/i.test(h1))return h1;
  var dt=(document.title||'').split(/[-–—|•]/)[0].replace(/\b(ios|android|web|app|screens|ui|patterns|mobbin)\b/gi,'').trim();
  if(dt&&dt.length>1)return dt;
  return '';
}

var rawSlug=getAppSlug();
if(!rawSlug||/^(app|apps|browse|loading)$/i.test(rawSlug)){
  rawSlug=prompt("Could not detect app name automatically. Please enter app name:","");
  if(!rawSlug){alert("Extraction cancelled: App name is required.");window.__mobbin_web_harvester_running=false;return;}
}
var appSlug=rawSlug.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,'');

function getMobbinCategory(){
  try{
    var nData=window.__NEXT_DATA__&&window.__NEXT_DATA__.props&&window.__NEXT_DATA__.props.pageProps;
    var nApp=nData&&(nData.app||(nData.data&&nData.data.app));
    if(nApp){
      if(Array.isArray(nApp.categories)&&nApp.categories.length){
        return nApp.categories.map(function(c){return typeof c==='string'?c:(c.name||'');}).filter(Boolean).join(', ');
      }
      if(nApp.category)return typeof nApp.category==='string'?nApp.category:(nApp.category.name||'');
    }
  }catch(e){}
  var catLinks=Array.from(document.querySelectorAll('a[href*="/categories/"], a[href*="/category/"], a[href*="category="], a[href*="categories="]'));
  if(catLinks.length>0){
    var cats=catLinks.map(function(a){return a.textContent.trim();}).filter(Boolean);
    if(cats.length)return Array.from(new Set(cats)).join(', ');
  }
  var all=Array.from(document.querySelectorAll('dt, dd, span, div, p, h4, h5, h6, label'));
  var label=all.find(function(e){return e.children.length===0&&/^categor(y|ies)$/i.test(e.textContent.trim());});
  if(label){
    if(label.nextElementSibling&&label.nextElementSibling.textContent.trim()){return label.nextElementSibling.textContent.trim();}
    var parent=label.parentElement;
    if(parent){
      var others=Array.from(parent.children).filter(function(e){return e!==label&&e.textContent.trim();});
      if(others.length>0)return others[0].textContent.trim();
      if(parent.nextElementSibling&&parent.nextElementSibling.textContent.trim()){return parent.nextElementSibling.textContent.trim();}
    }
  }
  var el=document.querySelector('header, main')||document.body;
  var m=el.innerText?el.innerText.match(/Categor(?:y|ies)\s*\n+([^\n]+)/i):null;
  if(m&&m[1])return m[1].trim();
  return '';
}

var catRaw=getMobbinCategory();
var catSlug=catRaw?catRaw.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,''):'';

var setMsg=function(t,s){
  box.innerHTML='<div style="font-weight:bold;font-size:15px;color:#60a5fa;margin-bottom:6px;">🌐 '+appSlug+(catRaw?' ('+catRaw+')':'')+'</div><div style="font-size:13px;margin-bottom:4px;">'+t+'</div><div style="font-size:12px;color:#9ca3af;">'+(s||'')+'</div>';
};

document.body.appendChild(box);

try{
  setMsg('Loading engine...','');
  if(typeof JSZip==='undefined'){
    await new Promise(function(res,rej){
      var s=document.createElement('script');
      s.src='https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
      s.onload=res;s.onerror=rej;document.head.appendChild(s);
    });
  }

  function getCutoffY(){
    var h=Array.from(document.querySelectorAll('h2, h3, h4, p, span, section')).find(function(e){return/more like|similar apps|related apps|you might like|more from|more in\s+[a-z]+/i.test(e.textContent||'')&&e.children.length<=1;});
    return h?(h.getBoundingClientRect().top+window.scrollY):Infinity;
  }

  var candidates=new Set();
  function harvest(){
    var cutoffY=getCutoffY();
    var root=document.querySelector('main')||document.body;
    var imgs=root.querySelectorAll('img[data-sentry-element="CdnImg"], img[alt*="screen" i], li div img');
    imgs.forEach(function(img){
      if(img.closest('header, nav, footer, [role="navigation"], [role="banner"], [role="dialog"], [data-radix-popper-content-wrapper]')){return;}
      var imgY=img.getBoundingClientRect().top+window.scrollY;
      if(imgY>=cutoffY)return;
      if(img.naturalWidth>0&&img.naturalWidth<100)return;
      // WEB filter (mobile kept portrait-only): accept landscape viewport shots
      // AND tall full-page captures; reject only extreme phone-portrait shapes.
      if(img.naturalWidth>0&&img.naturalHeight>0&&img.naturalHeight>img.naturalWidth*2.3){return;}
      var best=img.src;
      if(img.srcset){
        var c=img.srcset.split(',').map(function(s){var parts=s.trim().split(/\s+/);return{u:parts[0],w:parts[1]?parseInt(parts[1]):0};});
        c.sort(function(a,b){return b.w-a.w;});
        if(c[0]&&c[0].u)best=c[0].u;
      }
      if(best&&best.includes('bytescale.mobbin.com')){candidates.add(best);}
    });
  }

  setMsg('Phase 1: Scanning web screens...','Auto-scrolling until recommendations');
  var idle=0,lastCount=0;
  while(idle<6){
    harvest();
    setMsg('Phase 1: Scanning web screens...','Found '+candidates.size+' screens');
    var cutoffY=getCutoffY();
    if(window.scrollY+window.innerHeight>=cutoffY-100)break;
    window.scrollBy(0,window.innerHeight*1.5);
    await new Promise(function(r){setTimeout(r,400);});
    harvest();
    if(candidates.size===lastCount)idle++;else{idle=0;lastCount=candidates.size;}
  }
  window.scrollTo(0,0);
  var list=Array.from(candidates);
  if(!list.length){setMsg('❌ No valid web screens found','');cleanup();return;}

  setMsg('Phase 2: Downloading & filtering...','Processing '+list.length+' screens');
  var zip=new JSZip();
  var validCount=0,skipped=0;
  var concurrency=6;
  async function worker(items){
    for(var i=0;i<items.length;i++){
      var it=items[i];
      try{
        var res=await fetch(it.url);
        var blob=await res.blob();
        if(blob.size>10000){validCount++;zip.file('screen_'+String(validCount).padStart(3,'0')+'.webp',blob);}else{skipped++;}
      }catch(e){skipped++;}
      if((validCount+skipped)%5===0||(validCount+skipped)===list.length){setMsg('Phase 2: Downloading ('+validCount+' sharp)...',skipped+' placeholders skipped');}
    }
  }
  var indexed=list.map(function(u,i){return{url:u,index:i+1};});
  var chunks=Array.from({length:concurrency},function(){return[];});
  indexed.forEach(function(it,i){chunks[i%concurrency].push(it);});
  await Promise.all(chunks.map(function(c){return worker(c);}));

  if(validCount===0){setMsg('⚠️ No high-res web screens found','All detected images were placeholders');cleanup();return;}

  setMsg('Phase 3: Uploading to project...','Routing to category: '+(catRaw||'auto'));
  var zipBlob=await zip.generateAsync({type:'blob'});
  try{
    var url='http://127.0.0.1:3848/save?app='+encodeURIComponent(appSlug)+'&category='+encodeURIComponent(catRaw);
    var res=await fetch(url,{method:'POST',body:zipBlob});
    var data=await res.json();
    var summaryMsg='Saved '+data.count+' new web screens'+(data.skipped?' ('+data.skipped+' duplicates skipped)':'')+' into '+data.target;
    setMsg('🎉 Success!',summaryMsg);
  }catch(err){
    console.warn('Local web bridge not responding, falling back to download:',err);
    var zipFileName=appSlug+(catSlug?'__'+catSlug:'')+'__webscreens.zip';
    var a=document.createElement('a');
    a.href=URL.createObjectURL(zipBlob);
    a.download=zipFileName;
    document.body.appendChild(a);a.click();a.remove();
    setMsg('✅ Saved to Downloads!','Start the Web bridge to auto-ingest -> '+(catRaw||'category')+'...');
  }
}catch(err){
  setMsg('❌ Error during extraction',err.message||String(err));
}finally{
  cleanup();
}
})();
