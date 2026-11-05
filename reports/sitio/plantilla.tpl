<!doctype html>
<html lang="es" data-lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#002a47">
<title>Chill Index y ganadería en Uruguay | Proyecto JAI 2026</title>
<meta name="description" content="Información, resultados y preguntas frecuentes del trabajo presentado en la 41ª Jornada Acadêmica Integrada (UFSM). Español y portugués.">
<style>
:root {
  color-scheme: light;
  /* Paleta: azul marino y naranja del logo de la JAI, cada uno en una escala de tonos. */
  --azul-950: #001f35; --azul-900: #002a47; --azul-800: #003255; --azul-700: #0b4a75; --azul-600: #1f6595;
  --azul-400: #6f9fc2; --azul-300: #a3c3da; --azul-200: #c9dde9; --azul-100: #e4eef5; --azul-50: #f3f8fb;
  --naranja-800: #8a4600; --naranja-700: #ad5800; --naranja-500: #f07d00; --naranja-300: #f6b26b; --naranja-200: #fad5ab; --naranja-100: #fdf1e3;
  --ink: #16222e; --muted: #52606d; --line: #d5dfe6; --bg: #fff;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --serif: Georgia, "Times New Roman", "Noto Serif", serif;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 66px; -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 17px/1.6 var(--sans); padding-bottom: calc(66px + env(safe-area-inset-bottom)); }
html[data-lang="es"] .pt, html[data-lang="pt"] .es { display: none !important; }
a { color: var(--azul-600); }
button { font-family: inherit; }
p { margin: 0 0 12px; }
.wrap { max-width: 760px; margin: 0 auto; padding: 0 16px; }

/* Barra superior */
.top { position: sticky; top: 0; z-index: 30; background: #fff; box-shadow: 0 1px 0 var(--line); }
.top-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; height: 56px; }
.brand { font: 700 18px/1 var(--serif); color: var(--azul-800); white-space: nowrap; }
.top-actions { display: flex; align-items: center; gap: 8px; }
.langs { display: flex; border: 1px solid var(--azul-800); border-radius: 6px; overflow: hidden; }
.langs button { min-width: 46px; min-height: 42px; border: 0; background: #fff; color: var(--azul-800); font-weight: 700; font-size: 14px; cursor: pointer; }
.langs button[aria-pressed="true"] { background: var(--azul-800); color: #fff; }
.icon-btn { width: 44px; height: 44px; display: grid; place-items: center; border: 1px solid var(--line); border-radius: 6px; background: #fff; color: var(--azul-800); cursor: pointer; }
.icon-btn svg { width: 19px; height: 19px; }
.progress { height: 2px; background: var(--naranja-500); width: 0; }

/* Logos */
.logos { display: flex; align-items: center; justify-content: space-between; gap: 18px; padding: 14px 16px; }
.logos img { display: block; height: auto; }
.logo-utec { width: 100px; }
.logo-jai { width: 132px; }

/* Portada */
.hero { position: relative; overflow: hidden; color: #fff; background: linear-gradient(160deg, var(--azul-950), var(--azul-800) 62%, var(--azul-700)); }
.contours { position: absolute; inset: 0; width: 100%; height: 100%; opacity: .16; }
.hero-inner { position: relative; z-index: 2; padding-top: 28px; padding-bottom: 34px; }
.kicker { display: block; font-size: 13px; line-height: 1.4; font-weight: 600; letter-spacing: .02em; color: var(--azul-200); margin-bottom: 22px; }
.team-label { font-size: 12px; letter-spacing: .12em; font-weight: 700; color: var(--naranja-300); margin: 0 0 8px; }
.names { list-style: none; margin: 0 0 24px; padding: 0 0 20px; display: grid; gap: 4px; border-bottom: 1px solid rgba(255, 255, 255, .24); }
.names li { font-weight: 600; font-size: 16px; line-height: 1.4; }
h1 { font: 700 30px/1.18 var(--serif); margin: 0 0 22px; }
.cta { display: flex; flex-wrap: wrap; gap: 10px; }
.btn { display: inline-flex; align-items: center; justify-content: center; min-height: 46px; padding: 0 18px; border-radius: 6px; font-weight: 700; font-size: 15px; text-decoration: none; }
.btn-main { background: var(--naranja-500); color: var(--azul-950); }
.btn-ghost { border: 1px solid rgba(255, 255, 255, .55); color: #fff; }

/* Secciones */
section { padding: 36px 0; }
.tint-ice, .tint-green, .tint-violet { background: var(--azul-50); }
.tint-orange { background: #fff; }
.head { margin-bottom: 16px; padding-bottom: 10px; border-bottom: 2px solid var(--azul-800); }
.eyebrow { font-size: 12px; letter-spacing: .12em; font-weight: 700; color: var(--naranja-700); margin-bottom: 3px; }
h2 { font: 700 26px/1.2 var(--serif); margin: 0; color: var(--azul-800); }
h3 { font: 700 20px/1.25 var(--serif); margin: 22px 0 8px; color: var(--azul-800); }
.card { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 18px 16px; margin: 16px 0; }
.note { font-size: 14px; line-height: 1.5; color: var(--muted); }
.reveal { transition: opacity .4s ease; }
.js .reveal:not(.in) { opacity: 0; }

/* Respuesta y cifras */
#resumen { padding-top: 26px; }
.answer { border-left: 4px solid var(--naranja-500); padding: 2px 0 2px 16px; }
.answer .big { font: 700 22px/1.25 var(--serif); color: var(--azul-800); margin-bottom: 8px; }
.stats { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; margin: 22px 0 0; background: var(--line); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.stat { background: #fff; padding: 14px; }
.stat b { display: block; font: 700 30px/1.05 var(--sans); letter-spacing: -.01em; color: var(--azul-800); }
.stat.s4 b { color: var(--naranja-700); }
.stat span { display: block; font-size: 13px; line-height: 1.3; margin-top: 5px; color: var(--muted); }

/* Calculadora */
.formula { font: italic 18px/1.5 "Times New Roman", var(--serif); text-align: center; background: #fff; border: 1px solid var(--line); border-radius: 6px; padding: 9px 6px; }
.presets { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 12px; }
.chip { min-height: 44px; padding: 0 13px; border: 1px solid var(--azul-300); border-radius: 6px; background: #fff; color: var(--azul-800); font-weight: 600; font-size: 14px; cursor: pointer; }
.chip[aria-pressed="true"] { background: var(--azul-800); border-color: var(--azul-800); color: #fff; }
.gauge { max-width: 300px; margin: 2px auto 0; }
.gauge svg { display: block; width: 100%; height: auto; }
#needle { transition: transform .4s ease; transform-origin: 150px 150px; }
.risk { text-align: center; margin: -4px 0 14px; }
.risk b { display: block; font: 700 40px/1 var(--sans); letter-spacing: -.01em; color: var(--azul-800); }
.risk-pill { display: inline-block; margin-top: 8px; padding: 5px 14px; border-radius: 4px; font-weight: 700; font-size: 14px; }
.calc label { display: block; font-weight: 600; font-size: 15px; margin-bottom: 11px; }
.calc output { float: right; font-weight: 700; color: var(--azul-700); }
.calc input[type="range"] { display: block; width: 100%; height: 36px; margin-top: 2px; accent-color: var(--azul-700); }

/* Método */
.steps { display: grid; gap: 0; margin: 14px 0; border-top: 1px solid var(--line); }
.step { display: flex; gap: 14px; align-items: flex-start; padding: 13px 0; border-bottom: 1px solid var(--line); }
.step i { flex: none; width: 24px; font: 700 21px/1.2 var(--sans); font-style: normal; color: var(--naranja-700); }
.step b { display: block; color: var(--azul-800); line-height: 1.3; margin-bottom: 2px; font-weight: 700; }
.step div > span { font-size: 15px; line-height: 1.45; color: var(--muted); }
.years { display: grid; grid-template-columns: repeat(9, 1fr); gap: 3px; margin: 10px 0; }
.years button { min-height: 44px; padding: 0; border: 0; border-radius: 4px; background: var(--azul-100); color: var(--azul-700); font-size: 11.5px; font-weight: 700; cursor: pointer; transition: background .25s; }
.years button.test { background: var(--naranja-500); color: var(--azul-950); }
.dept-cards { display: flex; gap: 10px; overflow-x: auto; padding: 4px 16px 10px; margin: 0 -16px; scroll-snap-type: x proximity; }
.dept { flex: 0 0 236px; scroll-snap-align: center; border-radius: 8px; padding: 13px; background: #fff; border: 1px solid var(--line); font-size: 14px; line-height: 1.55; }
.dept h4 { margin: 0; font: 700 17px/1.2 var(--serif); color: var(--azul-800); }
.dept small { display: block; color: var(--muted); margin-bottom: 7px; font-size: 13px; }
.dept b { font-weight: 700; }

/* Comparación antes de ver */
.quiz { background: var(--azul-50); border: 1px solid var(--azul-200); border-radius: 8px; padding: 18px 16px; margin: 16px 0; }
.quiz h3 { margin: 0 0 4px; }
.quiz .opts { display: grid; gap: 7px; margin-top: 10px; }
.quiz button { width: 100%; min-height: 48px; padding: 9px 13px; text-align: left; border: 1px solid var(--azul-300); border-radius: 6px; background: #fff; color: var(--azul-800); font-size: 15px; font-weight: 600; cursor: pointer; position: relative; overflow: hidden; }
.quiz button .fill { position: absolute; inset: 0 auto 0 0; width: 0; background: var(--azul-200); transition: width .6s ease; }
.quiz button .txt { position: relative; display: flex; justify-content: space-between; gap: 8px; }
.quiz button.best { border-color: var(--naranja-500); }
.quiz button.best .fill { background: var(--naranja-200); }
.quiz .verdict { margin: 12px 0 0; font-size: 15px; line-height: 1.45; }

/* Gráficos */
figure { margin: 12px 0 0; }
figcaption { font-size: 14px; line-height: 1.5; color: var(--muted); margin-top: 10px; }
.tabs { display: flex; gap: 0; margin-bottom: 12px; border-bottom: 1px solid var(--line); }
.tabs button { flex: 1; min-height: 44px; border: 0; border-bottom: 3px solid transparent; background: transparent; font-weight: 700; font-size: 13.5px; color: var(--muted); cursor: pointer; padding: 3px; line-height: 1.1; margin-bottom: -1px; }
.tabs button[aria-pressed="true"] { color: var(--azul-800); border-bottom-color: var(--naranja-500); }
.legend { display: flex; flex-wrap: wrap; gap: 5px 13px; font-size: 13px; margin-bottom: 8px; color: var(--muted); }
.legend i { display: inline-block; width: 11px; height: 11px; border-radius: 50%; margin-right: 5px; vertical-align: -1px; }
.frow { padding: 8px 0; border-bottom: 1px solid var(--azul-100); }
.frow.best-row { background: var(--naranja-100); margin: 0 -8px; padding: 8px; border-radius: 4px; border-bottom: 0; }
.fhead { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; font-size: 14px; line-height: 1.25; }
.fhead b { white-space: nowrap; font-weight: 700; }
.tag { display: inline-block; margin-left: 5px; color: var(--naranja-800); font-size: 12px; font-weight: 700; }
.track { position: relative; height: 18px; margin-top: 5px; }
.track .ref { position: absolute; top: 0; bottom: 0; border-left: 1.5px dashed var(--muted); }
.track .ci { position: absolute; top: 8px; height: 2.5px; }
.track .dot { position: absolute; top: 4px; width: 11px; height: 11px; margin-left: -5.5px; border-radius: 50%; }
svg.chart { display: block; width: 100%; height: auto; }
.heat { display: grid; grid-template-columns: 78px repeat(9, 1fr); gap: 2px; font-size: 10.5px; }
.heat .hd { text-align: center; color: var(--muted); font-weight: 600; padding: 2px 0; }
.heat .rw { font-size: 12px; font-weight: 600; display: flex; align-items: center; line-height: 1.05; }
.heat button { min-height: 34px; padding: 0; border: 0; border-radius: 2px; font-size: 10.5px; font-weight: 600; cursor: pointer; font-family: inherit; }
.heat button.on { outline: 2.5px solid var(--ink); }
.heat-detail { margin-top: 10px; padding: 9px 12px; background: var(--azul-50); border-radius: 6px; font-size: 14px; font-weight: 600; color: var(--azul-800); }
.bars { display: grid; gap: 12px; }
.bar-title { font-size: 14px; font-weight: 700; margin-bottom: 3px; }
.bar { display: flex; align-items: center; gap: 7px; font-size: 13px; margin-bottom: 3px; }
.bar i { display: block; height: 14px; }
.bar-label { flex: 0 0 104px; color: var(--muted); line-height: 1.1; }
.callout { display: flex; gap: 11px; padding: 14px; border-radius: 6px; background: var(--naranja-100); border: 1px solid var(--naranja-200); margin: 16px 0; font-size: 15px; line-height: 1.5; }
.callout svg { flex: none; width: 22px; height: 22px; color: var(--naranja-700); margin-top: 1px; }

/* Preguntas */
.search { display: block; width: 100%; min-height: 48px; padding: 0 14px; border: 1px solid var(--azul-300); border-radius: 6px; font: inherit; background: #fff; margin-bottom: 10px; }
.cats { display: flex; gap: 6px; overflow-x: auto; padding: 0 16px 8px; margin: 0 -16px 4px; }
.cats .chip { flex: none; }
details { background: #fff; border-top: 1px solid var(--line); }
details:last-of-type { border-bottom: 1px solid var(--line); }
summary { cursor: pointer; padding: 14px 34px 14px 12px; font-weight: 700; font-size: 16px; line-height: 1.35; list-style: none; position: relative; color: var(--azul-800); }
summary::-webkit-details-marker { display: none; }
summary::after { content: "+"; position: absolute; right: 12px; top: 11px; font-size: 22px; font-weight: 400; color: var(--naranja-700); }
details[open] summary::after { content: "–"; }
details > div { padding: 0 12px 6px; font-size: 16px; }
details ul { padding-left: 20px; margin: 0 0 10px; }
details li { margin-bottom: 4px; }
.gloss { display: grid; gap: 0; border-top: 1px solid var(--line); }
.gloss div { border-bottom: 1px solid var(--line); padding: 10px 0; font-size: 15px; line-height: 1.45; }
.gloss b { display: block; color: var(--azul-800); }
.links { display: grid; gap: 0; border-top: 1px solid var(--line); }
.links a { display: flex; align-items: center; justify-content: space-between; gap: 8px; min-height: 50px; padding: 8px 2px; border-bottom: 1px solid var(--line); color: var(--azul-800); text-decoration: none; font-weight: 600; font-size: 15px; }
.links a::after { content: "→"; font-size: 18px; color: var(--naranja-700); }
footer { padding: 18px 0 26px; font-size: 13px; line-height: 1.5; color: var(--muted); border-top: 1px solid var(--line); }

/* Navegación inferior */
.tabbar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 40; display: grid; grid-template-columns: repeat(5, 1fr); background: #fff; border-top: 1px solid var(--line); padding-bottom: env(safe-area-inset-bottom); }
.tabbar a { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; height: 60px; text-decoration: none; color: var(--muted); font-size: 11px; font-weight: 600; border-top: 2px solid transparent; margin-top: -1px; }
.tabbar svg { width: 21px; height: 21px; }
.tabbar a.on { color: var(--azul-800); border-top-color: var(--naranja-500); }
.toast { position: fixed; left: 50%; bottom: 76px; transform: translateX(-50%); z-index: 50; padding: 9px 15px; border-radius: 6px; background: var(--azul-900); color: #fff; font-size: 14px; font-weight: 600; opacity: 0; pointer-events: none; transition: opacity .25s; }
.toast.show { opacity: 1; }
a:focus-visible, button:focus-visible, summary:focus-visible, input:focus-visible { outline: 3px solid var(--naranja-500); outline-offset: 2px; }
@media (min-width: 620px) {
  h1 { font-size: 38px; }
  .names { grid-template-columns: 1fr 1fr; }
  .stats { grid-template-columns: repeat(4, 1fr); }
  .gloss { grid-template-columns: 1fr 1fr; column-gap: 24px; }
  .hero-inner { padding-top: 40px; padding-bottom: 46px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation: none !important; transition: none !important; }
  .js .reveal:not(.in) { opacity: 1; }
}
</style>
</head>
<body>
<div class="top">
  <div class="wrap top-row">
    <div class="brand">Chill Index</div>
    <div class="top-actions">
      <button class="icon-btn" type="button" id="share" aria-label="Compartir / Compartilhar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg></button>
      <div class="langs" role="group" aria-label="Idioma">
        <button type="button" data-set-lang="es" aria-pressed="true">ES</button>
        <button type="button" data-set-lang="pt" aria-pressed="false">PT</button>
      </div>
    </div>
  </div>
  <div class="progress" id="progress"></div>
</div>

<div class="wrap logos">
  <img class="logo-utec" src="{{logo_utec}}" width="{{logo_utec_w}}" height="{{logo_utec_h}}" alt="UTEC, Universidad Tecnológica">
  <img class="logo-jai" src="{{logo_jai}}" width="{{logo_jai_w}}" height="{{logo_jai_h}}" alt="Jornada Acadêmica Integrada, UFSM">
</div>

<header class="hero" id="inicio">
  <svg class="contours" viewBox="0 0 800 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true" fill="none" stroke="#fff" stroke-width="1.2"><path d="M-20 30C150 -30 280 80 430 20S690 -40 830 10"/><path d="M-20 64C150 4 280 114 430 54S690 -6 830 44"/><path d="M-20 98C150 38 280 148 430 88S690 28 830 78"/><path d="M-20 132C150 72 280 182 430 122S690 62 830 112"/><path d="M-20 166C150 106 280 216 430 156S690 96 830 146"/><path d="M-20 200C150 140 280 250 430 190S690 130 830 180"/><path d="M-20 234C150 174 280 284 430 224S690 164 830 214"/><path d="M-20 268C150 208 280 318 430 258S690 198 830 248"/><path d="M-20 302C150 242 280 352 430 292S690 232 830 282"/><path d="M-20 336C150 276 280 386 430 326S690 266 830 316"/><path d="M-20 370C150 310 280 420 430 360S690 300 830 350"/><path d="M-20 404C150 344 280 454 430 394S690 334 830 384"/><path d="M-20 438C150 378 280 488 430 428S690 368 830 418"/></svg>
  <div class="wrap hero-inner">
    <span class="kicker">41ª Jornada Acadêmica Integrada · UFSM</span>
    <p class="team-label">[[es:INTEGRANTES||pt:INTEGRANTES]]</p>
    <ul class="names">
      <li>Luisa Gabriela Flores Piñeyro</li>
      <li>Alejandra Daiana Ramírez Sempert</li>
      <li>Alvaro Martin Barreto Tacoronte</li>
      <li>Juan Pedro de León Sum</li>
    </ul>
    <h1>[[es:Análisis de sistema predictivo agroclimático de intensidad ganadera y riesgo de mortalidad||pt:Análise de sistema preditivo agroclimático de intensidade pecuária e risco de mortalidade]]</h1>
    <div class="cta">
      <a class="btn btn-main" href="#chill">[[es:Probar la calculadora||pt:Testar a calculadora]]</a>
      <a class="btn btn-ghost" href="#faq">[[es:Preguntas||pt:Perguntas]]</a>
    </div>
  </div>
</header>

<section id="resumen" style="padding-top:0">
  <div class="wrap">
    <div class="answer reveal">
      <p class="big">[[es:¿El clima predice mejor que la historia de cada departamento?||pt:O clima prevê melhor do que a história de cada departamento?]]</p>
      <p>[[es:<b>Con nueve años de datos, no.</b> Ningún modelo climático principal superó de forma robusta a la historia de cada departamento. La relación entre clima y mortalidad existe, pero viene sobre todo de años que afectan a todos a la vez.||pt:<b>Com nove anos de dados, não.</b> Nenhum modelo climático principal superou de forma robusta a história de cada departamento. A relação entre clima e mortalidade existe, mas vem sobretudo de anos que afetam todos ao mesmo tempo.]]</p>
      <p class="note" style="margin:0">[[es:Esto no significa que el clima no afecte a los animales: significa que no se detectó una mejora al predecir con estos datos anuales.||pt:Isso não significa que o clima não afete os animais: significa que não se detectou melhora ao prever com estes dados anuais.]]</p>
    </div>
    <div class="stats reveal">
      <div class="stat s1"><b>{{panel_filas}}</b><span>[[es:observaciones: 5 departamentos × 9 ejercicios||pt:observações: 5 departamentos × 9 exercícios]]</span></div>
      <div class="stat s2"><b>{{especificaciones}}</b><span>[[es:modelos evaluados fuera de muestra||pt:modelos avaliados fora da amostra]]</span></div>
      <div class="stat s3"><b>0 / 12</b><span>[[es:modelos principales con valor predictivo||pt:modelos principais com valor preditivo]]</span></div>
      <div class="stat s4"><b>{{ba_c2}}</b><span>[[es:exactitud de repetir el año anterior, la mejor||pt:acurácia de repetir o ano anterior, a melhor]]</span></div>
    </div>
  </div>
</section>

<section id="chill" class="tint-ice">
  <div class="wrap">
    <div class="head c-blue reveal">
      <div><div class="eyebrow">[[es:EL ÍNDICE||pt:O ÍNDICE]]</div><h2>[[es:¿Qué es el Chill Index?||pt:O que é o Chill Index?]]</h2></div>
    </div>
    <p>[[es:El frío, el viento y la lluvia aumentan la pérdida de calor de los ovinos. El Chill Index (CI) resume esa exposición en un número. INIA lo usa para evaluar el riesgo en corderos recién nacidos y en ovinos recién esquilados.||pt:O frio, o vento e a chuva aumentam a perda de calor dos ovinos. O Chill Index (CI) resume essa exposição em um número. O INIA o utiliza para avaliar o risco em cordeiros recém-nascidos e em ovinos recém-tosquiados.]]</p>
    <p class="formula">CI = (11,7 + 3,1√V)(40 − T) + 481<br>+ 418(1 − e<sup>−0,04P</sup>)</p>
    <div class="card calc reveal">
      <div class="presets" id="presets"></div>
      <div class="gauge">
        <svg viewBox="0 0 300 165" role="img" aria-labelledby="ci-class"><g id="gauge-arcs"></g>
          <g id="needle"><path d="M150 150 150 80" stroke="#003255" stroke-width="5" stroke-linecap="round"/></g><circle cx="150" cy="150" r="9" fill="#003255"/></svg>
      </div>
      <div class="risk" aria-live="polite"><b id="ci-value"></b><span class="risk-pill" id="ci-class"></span></div>
      <label for="ci-t">[[es:Temperatura media||pt:Temperatura média]] <output id="ci-t-o"></output><input id="ci-t" type="range" min="-5" max="35" step="0.5" value="6"></label>
      <label for="ci-v">[[es:Viento medio||pt:Vento médio]] <output id="ci-v-o"></output><input id="ci-v" type="range" min="0" max="12" step="0.5" value="4"></label>
      <label for="ci-p">[[es:Lluvia del día||pt:Chuva do dia]] <output id="ci-p-o"></output><input id="ci-p" type="range" min="0" max="60" step="1" value="0"></label>
      <p class="note" style="margin:0">[[es:Calculadora educativa con la fórmula de INIA (CI en kJ/m²/h). No reemplaza los pronósticos ni las alertas oficiales.||pt:Calculadora educativa com a fórmula do INIA (CI em kJ/m²/h). Não substitui as previsões nem os alertas oficiais.]]</p>
    </div>
  </div>
</section>

<section id="metodo" class="tint-green">
  <div class="wrap">
    <div class="head c-green reveal">
      <div><div class="eyebrow">[[es:CÓMO SE HIZO||pt:COMO FOI FEITO]]</div><h2>[[es:Datos y método||pt:Dados e método]]</h2></div>
    </div>
    <div class="steps">
      <div class="step reveal"><i>1</i><div><b>[[es:Clima diario de INIA||pt:Clima diário do INIA]]</b><span>[[es:Temperatura, lluvia y viento de una estación por departamento.||pt:Temperatura, chuva e vento de uma estação por departamento.]]</span></div></div>
      <div class="step reveal"><i>2</i><div><b>[[es:Declaraciones de SNIG/DICOSE||pt:Declarações do SNIG/DICOSE]]</b><span>[[es:Muertes, existencias, unidades ganaderas y superficie.||pt:Mortes, estoques, unidades pecuárias e área.]]</span></div></div>
      <div class="step reveal"><i>3</i><div><b>[[es:Panel de {{panel_filas}} observaciones||pt:Painel de {{panel_filas}} observações]]</b><span>[[es:Cinco departamentos por nueve ejercicios, de julio a junio.||pt:Cinco departamentos por nove exercícios, de julho a junho.]]</span></div></div>
      <div class="step reveal"><i>4</i><div><b>[[es:Modelos contra referencias simples||pt:Modelos contra referências simples]]</b><span>[[es:Ridge y logística frente al promedio, al año anterior y a un control sin clima.||pt:Ridge e logística frente à média, ao ano anterior e a um controle sem clima.]]</span></div></div>
    </div>
    <h3>[[es:Los departamentos||pt:Os departamentos]]</h3>
    <div class="dept-cards" id="dept-cards" tabindex="0" aria-label="Departamentos"></div>
    <p class="note">[[es:Media ± desvío estándar por ejercicio (n = 9). Deslice para ver todos.||pt:Média ± desvio-padrão por exercício (n = 9). Deslize para ver todos.]]</p>
    <div class="card reveal">
      <h3 style="margin-top:0">[[es:Cada año se predice sin haberlo visto||pt:Cada ano é previsto sem ter sido visto]]</h3>
      <div class="years" id="years"></div>
      <p class="note" style="margin:0" id="year-text" aria-live="polite"></p>
    </div>
  </div>
</section>

<section id="resultados" class="tint-orange">
  <div class="wrap">
    <div class="head c-orange reveal">
      <div><div class="eyebrow">[[es:QUÉ ENCONTRAMOS||pt:O QUE ENCONTRAMOS]]</div><h2>[[es:Resultados||pt:Resultados]]</h2></div>
    </div>

    <div class="quiz reveal">
      <h3>[[es:Antes de ver los resultados||pt:Antes de ver os resultados]]</h3>
      <p style="margin:0">[[es:¿Cuál cree que predijo mejor los años de mortalidad elevada? Elija una opción.||pt:O que você acha que previu melhor os anos de mortalidade elevada? Escolha uma opção.]]</p>
      <div class="opts" id="quiz-opts"></div>
      <p class="verdict" id="quiz-verdict" aria-live="polite"></p>
    </div>

    <div class="card reveal">
      <h3 style="margin-top:0">[[es:Predicción fuera de muestra||pt:Previsão fora da amostra]]</h3>
      <div class="tabs" id="forest-tabs"></div>
      <div class="legend" id="legend"></div>
      <div id="forest"></div>
      <figcaption id="forest-cap"></figcaption>
    </div>

    <div class="card reveal">
      <h3 style="margin-top:0">[[es:Los años se mueven en bloque||pt:Os anos se movem em bloco]]</h3>
      <div class="tabs" id="heat-tabs"></div>
      <div class="heat" id="heat"></div>
      <div class="heat-detail" id="heat-detail" aria-live="polite"></div>
      <figcaption>[[es:Anomalía respecto de la media de cada departamento (z): azul, por debajo; naranja, por encima.||pt:Anomalia em relação à média de cada departamento (z): azul, abaixo; laranja, acima.]]</figcaption>
    </div>

    <div class="card reveal">
      <h3 style="margin-top:0">[[es:Mortalidad por departamento||pt:Mortalidade por departamento]]</h3>
      <div class="presets" id="dept-chips"></div>
      <svg class="chart" id="linea" viewBox="0 0 360 230" role="img" aria-labelledby="linea-cap"></svg>
      <figcaption id="linea-cap">[[es:Muertes por mil ovinos (tasa aproximada). Línea oscura: promedio de los cinco. Bajan juntos en 2021–2023 y suben en 2024–2025.||pt:Mortes por mil ovinos (taxa aproximada). Linha escura: média dos cinco. Caem juntos em 2021–2023 e sobem em 2024–2025.]]</figcaption>
    </div>

    <div class="card reveal">
      <h3 style="margin-top:0">[[es:La señal está en el año, no en la región||pt:O sinal está no ano, não na região]]</h3>
      <p>[[es:Si además se descuenta lo común a cada año, la relación del Chill Index con la mortalidad casi desaparece. La información climática equivale a unos 9 años, no a 45 observaciones.||pt:Se também se desconta o que é comum a cada ano, a relação do Chill Index com a mortalidade quase desaparece. A informação climática equivale a cerca de 9 anos, não a 45 observações.]]</p>
      <div class="bars" id="correlaciones"></div>
      <figcaption>[[es:Correlación (r de Pearson) con la mortalidad ovina, 2017–2025.||pt:Correlação (r de Pearson) com a mortalidade ovina, 2017–2025.]]</figcaption>
    </div>

    <div class="callout reveal">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" aria-hidden="true"><path d="M12 8v5M12 17h.01"/><path d="M10.3 3.6 2 18a2 2 0 0 0 1.7 3h16.6a2 2 0 0 0 1.7-3L13.7 3.6a2 2 0 0 0-3.4 0z"/></svg>
      <div>[[es:<b>Cuidado al leerlo:</b> con tan pocos años, los intervalos son amplios y se superponen. El resultado es la ausencia de una mejora detectable, no una prueba de que el clima no importe.||pt:<b>Cuidado ao ler:</b> com tão poucos anos, os intervalos são amplos e se sobrepõem. O resultado é a ausência de uma melhora detectável, não uma prova de que o clima não importa.]]</div>
    </div>
  </div>
</section>

<section id="faq" class="tint-violet">
  <div class="wrap">
    <div class="head c-violet reveal">
      <div><div class="eyebrow">[[es:CONSULTAS||pt:CONSULTAS]]</div><h2>[[es:Preguntas frecuentes||pt:Perguntas frequentes]]</h2></div>
    </div>
    <label class="es" for="faq-search-es" style="display:block"><input class="search" id="faq-search-es" type="search" placeholder="Buscar una pregunta…" aria-label="Buscar una pregunta"></label>
    <label class="pt" for="faq-search-pt" style="display:block"><input class="search" id="faq-search-pt" type="search" placeholder="Buscar uma pergunta…" aria-label="Buscar uma pergunta"></label>
    <div class="cats" id="faq-cats"></div>
    <p class="note" id="faq-empty" hidden>[[es:No encontramos esa pregunta. Puede consultarla al equipo en el stand.||pt:Não encontramos essa pergunta. Consulte a equipe no estande.]]</p>

    <details data-cat="res"><summary>[[es:Entonces, ¿el clima no afecta a las ovejas?||pt:Então o clima não afeta as ovelhas?]]</summary><div><p>[[es:No es lo que concluimos. El frío, el viento y la lluvia pueden afectar a los animales. Lo que encontramos es que, con datos anuales y agregados por departamento, el clima no mejora la predicción de un año nuevo. El estudio tampoco mide causas.||pt:Não é o que concluímos. O frio, o vento e a chuva podem afetar os animais. O que encontramos é que, com dados anuais e agregados por departamento, o clima não melhora a previsão de um ano novo. O estudo também não mede causas.]]</p></div></details>
    <details data-cat="res"><summary>[[es:¿Por qué presentar un resultado negativo?||pt:Por que apresentar um resultado negativo?]]</summary><div><p>[[es:Porque también es conocimiento útil: evita prometer una herramienta que no funciona con estos datos y muestra qué información haría falta. Aceptar ese resultado era un criterio definido desde el inicio del proyecto.||pt:Porque também é conhecimento útil: evita prometer uma ferramenta que não funciona com estes dados e mostra qual informação seria necessária. Aceitar esse resultado era um critério definido desde o início do projeto.]]</p></div></details>
    <details data-cat="res"><summary>[[es:¿Qué es la persistencia y por qué gana?||pt:O que é a persistência e por que ela vence?]]</summary><div><p>[[es:Es predecir que este año será como el anterior. Funciona bien porque estos indicadores cambian despacio: la intensidad tiene una correlación de {{r_int_lag}} con el año anterior. Si un modelo no supera esta regla simple, no aporta valor predictivo.||pt:É prever que este ano será como o anterior. Funciona bem porque estes indicadores mudam devagar: a intensidade tem correlação de {{r_int_lag}} com o ano anterior. Se um modelo não supera essa regra simples, não agrega valor preditivo.]]</p></div></details>
    <details data-cat="met"><summary>[[es:¿Por qué solo {{panel_filas}} observaciones, si hay cientos de miles de registros?||pt:Por que só {{panel_filas}} observações, se há centenas de milhares de registros?]]</summary><div><p>[[es:Las {{filas_ovinas}} filas ovinas de los cinco departamentos comparten el mismo clima departamental dentro de cada año. Tratarlas como independientes inflaría artificialmente la muestra y daría resultados demasiado optimistas (pseudorreplicación). Por eso se agregan por departamento y ejercicio.||pt:As {{filas_ovinas}} linhas ovinas dos cinco departamentos compartilham o mesmo clima departamental em cada ano. Tratá-las como independentes inflaria artificialmente a amostra e daria resultados otimistas demais (pseudorreplicação). Por isso são agregadas por departamento e exercício.]]</p></div></details>
    <details data-cat="met"><summary>[[es:¿Qué significa «dejar un año afuera»?||pt:O que significa «deixar um ano de fora»?]]</summary><div><p>[[es:Para evaluar 2022, por ejemplo, el modelo aprende de los otros años y nunca ve 2022. Después se compara su predicción con lo que realmente pasó. Se repite con cada año. Así se simula predecir un año desconocido.||pt:Para avaliar 2022, por exemplo, o modelo aprende com os outros anos e nunca vê 2022. Depois sua previsão é comparada com o que realmente aconteceu. Repete-se com cada ano. Assim se simula prever um ano desconhecido.]]</p></div></details>
    <details data-cat="met"><summary>[[es:¿Qué limitaciones tiene el estudio?||pt:Quais são as limitações do estudo?]]</summary><div><ul>
      <li>[[es:Mortalidad anual, sin fecha ni categoría animal.||pt:Mortalidade anual, sem data nem categoria animal.]]</li>
      <li>[[es:Una sola estación climática por departamento.||pt:Uma só estação climática por departamento.]]</li>
      <li>[[es:Existencias declaradas al cierre, no los animales expuestos durante todo el año. No se evaluó aún el denominador alternativo.||pt:Estoques declarados no fechamento, não os animais expostos durante todo o ano. O denominador alternativo ainda não foi avaliado.]]</li>
      <li>[[es:Solo nueve años, con muchas comparaciones entre modelos.||pt:Apenas nove anos, com muitas comparações entre modelos.]]</li>
      <li>[[es:Datos observacionales: no permiten afirmar causas.||pt:Dados observacionais: não permitem afirmar causas.]]</li>
    </ul></div></details>
    <details data-cat="uso"><summary>[[es:¿Un productor puede usar esto hoy?||pt:Um produtor pode usar isto hoje?]]</summary><div><p>[[es:No: no es un sistema de alerta. Para decisiones en el campo, como el manejo en parición o después de la esquila, conviene consultar los pronósticos y recomendaciones de INIA y de los técnicos.||pt:Não: não é um sistema de alerta. Para decisões no campo, como o manejo na parição ou depois da tosquia, convém consultar as previsões e recomendações do INIA e dos técnicos.]]</p></div></details>
    <details data-cat="uso"><summary>[[es:¿Vale para corderos, para todo Uruguay o para otros países?||pt:Vale para cordeiros, para todo o Uruguai ou para outros países?]]</summary><div><p>[[es:No se puede extrapolar. Los datos cubren la mortalidad de todos los ovinos, sin separar corderos, y solo cinco departamentos con estación de INIA. Probarlo en otras regiones, como el sur de Brasil, requeriría sus propios datos y una nueva validación.||pt:Não se pode extrapolar. Os dados cobrem a mortalidade de todos os ovinos, sem separar cordeiros, e apenas cinco departamentos com estação do INIA. Testar em outras regiões, como o sul do Brasil, exigiria dados próprios e uma nova validação.]]</p></div></details>
    <details data-cat="uso"><summary>[[es:Si el título dice «sistema predictivo», ¿dónde está el sistema?||pt:Se o título diz «sistema preditivo», onde está o sistema?]]</summary><div><p>[[es:El título es el del resumen aceptado. El trabajo se planteó primero como una evaluación rigurosa: comprobar si el clima realmente predice, antes de construir una herramienta. Como no se comprobó, esta versión no incluye un sistema operativo ni un panel de visualización.||pt:O título é o do resumo aceito. O trabalho foi conduzido primeiro como uma avaliação rigorosa: verificar se o clima realmente prevê, antes de construir uma ferramenta. Como isso não se confirmou, esta versão não inclui um sistema operacional nem um painel de visualização.]]</p></div></details>
    <details data-cat="uso"><summary>[[es:¿Qué haría falta para responder mejor?||pt:O que seria necessário para responder melhor?]]</summary><div><ul>
      <li>[[es:Mortalidad con fecha y por categoría, sobre todo de corderos.||pt:Mortalidade com data e por categoria, sobretudo de cordeiros.]]</li>
      <li>[[es:Series históricas más largas.||pt:Séries históricas mais longas.]]</li>
      <li>[[es:Clima en grilla espacial, con variación dentro de cada departamento.||pt:Clima em grade espacial, com variação dentro de cada departamento.]]</li>
      <li>[[es:Más departamentos para validar los resultados afuera de la muestra original.||pt:Mais departamentos para validar os resultados fora da amostra original.]]</li>
    </ul></div></details>
    <details data-cat="uso"><summary>[[es:¿Puedo ver los datos y el código?||pt:Posso ver os dados e o código?]]</summary><div><p>[[es:Sí. El código, los datos de entrada, los resultados de cada corrida y el informe están en el <a href="https://github.com/alejandra-ramirez-000/Proyecto_JAI">repositorio público</a>. Las instrucciones para reproducir todo están en el README.||pt:Sim. O código, os dados de entrada, os resultados de cada execução e o relatório estão no <a href="https://github.com/alejandra-ramirez-000/Proyecto_JAI">repositório público</a>. As instruções para reproduzir tudo estão no README.]]</p></div></details>
  </div>
</section>

<section id="mas">
  <div class="wrap">
    <div class="head c-navy reveal">
      <div><div class="eyebrow">[[es:PARA PROFUNDIZAR||pt:PARA SE APROFUNDAR]]</div><h2>[[es:Glosario y enlaces||pt:Glossário e links]]</h2></div>
    </div>
    <div class="gloss" id="glosario">
      <div><b>[[es:Exactitud balanceada||pt:Acurácia balanceada]]</b>[[es:Promedio de los aciertos en cada clase. 0,5 equivale a no distinguir nada.||pt:Média dos acertos em cada classe. 0,5 equivale a não distinguir nada.]]</div>
      <div><b>Baseline</b>[[es:Método simple que un modelo debe superar para aportar valor.||pt:Método simples que um modelo deve superar para agregar valor.]]</div>
      <div><b>[[es:Ejercicio ganadero||pt:Exercício pecuário]]</b>[[es:Período del 1 de julio al 30 de junio siguiente.||pt:Período de 1º de julho a 30 de junho seguinte.]]</div>
      <div><b>[[es:Error absoluto medio||pt:Erro absoluto médio]]</b>[[es:Diferencia promedio entre lo predicho y lo observado.||pt:Diferença média entre o previsto e o observado.]]</div>
      <div><b>[[es:Fuera de muestra||pt:Fora da amostra]]</b>[[es:Evaluado con datos que el modelo no vio al entrenarse.||pt:Avaliado com dados que o modelo não viu no treinamento.]]</div>
      <div><b>[[es:Intervalo de confianza del 95 %||pt:Intervalo de confiança de 95 %]]</b>[[es:Rango de valores compatibles con los datos; aquí, remuestreando años completos.||pt:Faixa de valores compatíveis com os dados; aqui, reamostrando anos completos.]]</div>
      <div><b>[[es:Unidad ganadera (UG)||pt:Unidade pecuária (UG)]]</b>[[es:Medida que permite sumar animales de distinto tipo y tamaño.||pt:Medida que permite somar animais de diferentes tipos e tamanhos.]]</div>
    </div>
    <h3>[[es:Enlaces||pt:Links]]</h3>
    <div class="links">
      <a href="https://github.com/alejandra-ramirez-000/Proyecto_JAI/blob/main/reports/informe_final.md">[[es:Informe completo (en español)||pt:Relatório completo (em espanhol)]]</a>
      <a href="https://github.com/alejandra-ramirez-000/Proyecto_JAI">[[es:Código y datos en GitHub||pt:Código e dados no GitHub]]</a>
      <a href="https://inia.uy/gras/Aplicaciones_y_recursos/Prevision%20Corderos">[[es:INIA: previsión para corderos||pt:INIA: previsão para cordeiros]]</a>
      <a href="https://catalogodatos.gub.uy/es/dataset/mgap-datos-preliminares-basados-en-la-declaracion-jurada-de-existencias-dicose-snig-2024">[[es:Datos abiertos SNIG/DICOSE||pt:Dados abertos SNIG/DICOSE]]</a>
    </div>
    <p style="margin:18px 0 0;font-weight:700;color:var(--navy)">[[es:Para otras consultas, hable con el equipo en el stand.||pt:Para outras consultas, fale com a equipe no estande.]]</p>
  </div>
</section>

<footer>
  <div class="wrap">[[es:Proyecto de Aprendizaje Automático, Licenciatura en Ingeniería de Datos e Inteligencia Artificial, UTEC. Fuentes de datos: INIA y MGAP/SNIG. Las cifras provienen de la corrida {{run}} del repositorio.||pt:Projeto de Aprendizado de Máquina, Licenciatura em Engenharia de Dados e Inteligência Artificial, UTEC. Fontes de dados: INIA e MGAP/SNIG. Os números provêm da execução {{run}} do repositório.]]</div>
</footer>

<nav class="tabbar" aria-label="Secciones">
  <a href="#inicio" data-spy="inicio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="m3 11 9-8 9 8v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>[[es:Inicio||pt:Início]]</a>
  <a href="#chill" data-spy="chill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 2v20M3.3 7l17.4 10M20.7 7 3.3 17"/></svg>[[es:Calcular||pt:Calcular]]</a>
  <a href="#metodo" data-spy="metodo"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6L4.8 18a2 2 0 0 0 1.8 3h10.8a2 2 0 0 0 1.8-3L14 9V3"/></svg>[[es:Método||pt:Método]]</a>
  <a href="#resultados" data-spy="resultados"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>[[es:Resultados||pt:Resultados]]</a>
  <a href="#faq" data-spy="faq"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 9a3 3 0 1 1 4.5 2.6c-1 .6-1.5 1.2-1.5 2.4M12 18h.01"/><circle cx="12" cy="12" r="10"/></svg>[[es:Preguntas||pt:Perguntas]]</a>
</nav>
<div class="toast" id="toast" role="status"></div>

<script>
document.documentElement.classList.add("js");
const DATA = /*__DATOS__*/null;
const TEXT = {
  es: { all: "Todos", base: "referencia", control: "sin clima", climate: "con clima", best: "mejor", mean: "Promedio",
    classes: ["Sin riesgo", "Riesgo bajo", "Riesgo medio", "Riesgo alto", "Condiciones críticas"],
    presets: ["Día templado", "Mañana fría", "Temporal"],
    intensity: "Intensidad", mortality: "Mortalidad", ci: "Días CI ≥ 1000", precip: "Lluvia",
    capReg: "Error absoluto medio en UG/ha, fuera de muestra (n = 40). Menor es mejor. Barra: intervalo de confianza del 95 %. Línea punteada: persistencia. Sumar clima al año anterior aumenta el error cerca de {{skill}} %.",
    capCls: "Exactitud balanceada, fuera de muestra (n = 40). Mayor es mejor. Barra: intervalo de confianza del 95 %. Línea punteada: 0,5, equivalente al azar. Las estimaciones con Chill Index quedan por debajo.",
    labels: { intensidad: "Intensidad", mortalidad: "Mortalidad", stock: "Existencias", u: { intensidad: "UG/ha", mortalidad: "‰", stock: "mil" } },
    years: (y) => `Se predice ${y} con los otros ocho años; sus cinco departamentos quedan afuera del entrenamiento. Toque otro año para verlo. Esta validación se llama Leave-One-Year-Out.`,
    quizOpts: ["El Chill Index", "El clima básico", "Lo que pasó el año anterior"],
    right: "Correcto. La persistencia fue la mejor referencia, porque los años elevados tienden a agruparse.",
    wrong: "La mejor fue la persistencia, porque los años elevados tienden a agruparse.",
    heatUnit: { mort: "muertes por mil", ci: "días con CI ≥ 1000", precip: "mm de lluvia" }, tap: "Toque una celda para ver el valor.",
    cats: { all: "Todas", res: "Resultados", met: "Método", uso: "Uso" }, var: { ci1000: "Días con CI ≥ 1000", ci1200: "Días con CI ≥ 1200", precip: "Precipitación" },
    global: "Global", intra: "Por departamento", intraYear: "Por depto. y año", copied: "Enlace copiado", shareTitle: "Chill Index y ganadería en Uruguay" },
  pt: { all: "Todos", base: "referência", control: "sem clima", climate: "com clima", best: "melhor", mean: "Média",
    classes: ["Sem risco", "Risco baixo", "Risco médio", "Risco alto", "Condições críticas"],
    presets: ["Dia ameno", "Manhã fria", "Temporal"],
    intensity: "Intensidade", mortality: "Mortalidade", ci: "Dias CI ≥ 1000", precip: "Chuva",
    capReg: "Erro absoluto médio em UG/ha, fora da amostra (n = 40). Menor é melhor. Barra: intervalo de confiança de 95 %. Linha tracejada: persistência. Somar clima ao ano anterior aumenta o erro em cerca de {{skill}} %.",
    capCls: "Acurácia balanceada, fora da amostra (n = 40). Maior é melhor. Barra: intervalo de confiança de 95 %. Linha tracejada: 0,5, equivalente ao acaso. As estimativas com Chill Index ficam abaixo.",
    labels: { intensidad: "Intensidade", mortalidad: "Mortalidade", stock: "Estoque", u: { intensidad: "UG/ha", mortalidad: "‰", stock: "mil" } },
    years: (y) => `Prevê-se ${y} com os outros oito anos; seus cinco departamentos ficam fora do treinamento. Toque em outro ano para vê-lo. Essa validação se chama Leave-One-Year-Out.`,
    quizOpts: ["O Chill Index", "O clima básico", "O que aconteceu no ano anterior"],
    right: "Correto. A persistência foi a melhor referência, porque os anos elevados tendem a se agrupar.",
    wrong: "A melhor foi a persistência, porque os anos elevados tendem a se agrupar.",
    heatUnit: { mort: "mortes por mil", ci: "dias com CI ≥ 1000", precip: "mm de chuva" }, tap: "Toque em uma célula para ver o valor.",
    cats: { all: "Todas", res: "Resultados", met: "Método", uso: "Uso" }, var: { ci1000: "Dias com CI ≥ 1000", ci1200: "Dias com CI ≥ 1200", precip: "Precipitação" },
    global: "Global", intra: "Por departamento", intraYear: "Por depto. e ano", copied: "Link copiado", shareTitle: "Chill Index e pecuária no Uruguai" },
};
const COLORS = { base: "#8fa3b3", control: "#003255", climate: "#d96f00" };
// Riesgo: un solo tono de naranja, de claro a oscuro.
const RISK = ["#fad5ab", "#f6b26b", "#f07d00", "#ad5800", "#6b3600"];
const RISK_INK = ["#16222e", "#16222e", "#16222e", "#fff", "#fff"];
const CI_LIMITS = [900, 1000, 1100, 1200];
const CI_MIN = 700, CI_MAX = 1400;
const PRESETS = [[22, 2, 0], [6, 4, 0], [4, 8, 30]];
let lang = "es", deptSel = null, forestKind = "reg", heatKind = "mort", heatCell = null, yearSel = 0, yearTimer = null, quizPick = null, faqCat = "all", faqText = "";

const el = (id) => document.getElementById(id);
const dec = (v, d) => v.toFixed(d).replace(".", ",").replace("-", "−");
const t = () => TEXT[lang];
const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

function pickLang() {
  const q = new URLSearchParams(location.search).get("lang");
  if (q === "es" || q === "pt") return q;
  try { const s = localStorage.getItem("jai-lang"); if (s === "es" || s === "pt") return s; } catch (e) { /* sin almacenamiento */ }
  return (navigator.language || "es").toLowerCase().startsWith("pt") ? "pt" : "es";
}
function setLang(value) {
  lang = value;
  document.documentElement.lang = value === "pt" ? "pt-BR" : "es";
  document.documentElement.dataset.lang = value;
  document.querySelectorAll("[data-set-lang]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.setLang === value)));
  try { localStorage.setItem("jai-lang", value); } catch (e) { /* sin almacenamiento */ }
  renderAll();
}

/* Calculadora */
function polar(v, r) {
  const a = Math.PI * (1 - (v - CI_MIN) / (CI_MAX - CI_MIN));
  return [150 + r * Math.cos(a), 150 - r * Math.sin(a)];
}
function drawGauge() {
  const edges = [CI_MIN, ...CI_LIMITS, CI_MAX];
  let svg = "";
  edges.slice(0, -1).forEach((from, i) => {
    const [x1, y1] = polar(from + 2, 118), [x2, y2] = polar(edges[i + 1] - 2, 118);
    svg += `<path d="M${x1} ${y1}A118 118 0 0 1 ${x2} ${y2}" fill="none" stroke="${RISK[i]}" stroke-width="20"/>`;
  });
  CI_LIMITS.forEach((v) => {
    const [x, y] = polar(v, 90);
    svg += `<text x="${x}" y="${y + 4}" text-anchor="middle" font-size="12" font-weight="700" font-family="Arial" fill="#52606d">${v}</text>`;
  });
  el("gauge-arcs").innerHTML = svg;
}
function chillIndex(T, V, P) { return (11.7 + 3.1 * Math.sqrt(V)) * (40 - T) + 481 + 418 * (1 - Math.exp(-0.04 * P)); }
function renderCalc() {
  const T = +el("ci-t").value, V = +el("ci-v").value, P = +el("ci-p").value;
  el("ci-t-o").textContent = dec(T, 1) + " °C";
  el("ci-v-o").textContent = dec(V, 1) + " m/s";
  el("ci-p-o").textContent = P + " mm";
  const ci = chillIndex(T, V, P);
  const k = CI_LIMITS.filter((l) => ci >= l).length;
  el("ci-value").textContent = Math.round(ci).toLocaleString("es-UY");
  el("ci-class").textContent = t().classes[k];
  el("ci-class").style.background = RISK[k];
  el("ci-class").style.color = RISK_INK[k];
  const clamped = Math.max(CI_MIN, Math.min(CI_MAX, ci));
  el("needle").style.transform = `rotate(${-90 + (180 * (clamped - CI_MIN)) / (CI_MAX - CI_MIN)}deg)`;
  document.querySelectorAll("#presets button").forEach((b, i) => {
    const [a, c, d] = PRESETS[i];
    b.setAttribute("aria-pressed", String(a === T && c === V && d === P));
  });
}
function renderPresets() {
  el("presets").innerHTML = t().presets.map((name) => `<button class="chip" type="button">${name}</button>`).join("");
  el("presets").querySelectorAll("button").forEach((b, i) => b.addEventListener("click", () => {
    const [T, V, P] = PRESETS[i];
    el("ci-t").value = T; el("ci-v").value = V; el("ci-p").value = P;
    renderCalc();
  }));
}

/* Departamentos */
function renderDepts() {
  const L = t().labels;
  el("dept-cards").innerHTML = DATA.departamentos.map((d) => `<article class="dept"><h4>${d.nombre}</h4><small>${d.estacion}</small>
    ${["intensidad", "mortalidad", "stock"].map((k) => `${L[k]}: <b>${d[k]}</b> ${L.u[k]}`).join("<br>")}</article>`).join("");
}

/* Validación */
function renderYears() {
  el("years").innerHTML = DATA.anios.map((y, i) => `<button type="button" class="${i === yearSel ? "test" : ""}" aria-pressed="${i === yearSel}" aria-label="${y}">’${String(y).slice(2)}</button>`).join("");
  el("year-text").textContent = t().years(DATA.anios[yearSel]);
  el("years").querySelectorAll("button").forEach((b, i) => b.addEventListener("click", () => {
    clearInterval(yearTimer); yearTimer = null;
    yearSel = i; renderYears();
  }));
}

/* Juego */
function renderQuiz() {
  const rows = DATA.clasificacion;
  const value = (key) => rows.find((r) => r.id === key).v;
  const opts = [
    { label: t().quizOpts[0], v: value("logistica_B_ejercicio") },
    { label: t().quizOpts[1], v: value("logistica_A_ejercicio") },
    { label: t().quizOpts[2], v: value("C2_persistencia_riesgo"), best: true },
  ];
  el("quiz-opts").innerHTML = opts.map((o, i) => `<button type="button" class="${quizPick !== null && o.best ? "best" : ""}" aria-pressed="${quizPick === i}"><span class="fill" style="width:${quizPick === null ? 0 : o.v * 100}%"></span><span class="txt"><span>${o.label}</span><b>${quizPick === null ? "" : dec(o.v, 2)}</b></span></button>`).join("");
  el("quiz-verdict").textContent = quizPick === null ? "" : (opts[quizPick].best ? t().right : t().wrong);
  el("quiz-opts").querySelectorAll("button").forEach((b, i) => b.addEventListener("click", () => { quizPick = i; renderQuiz(); }));
}

/* Forest */
function tabsOf(id, items, current, onPick) {
  el(id).innerHTML = items.map(([key, label]) => `<button type="button" data-k="${key}" aria-pressed="${key === current}">${label}</button>`).join("");
  el(id).querySelectorAll("button").forEach((b) => b.addEventListener("click", () => onPick(b.dataset.k)));
}
function renderForest() {
  tabsOf("forest-tabs", [["reg", t().intensity], ["cls", t().mortality]], forestKind, (k) => { forestKind = k; renderForest(); });
  el("legend").innerHTML = [["base", t().base], ["control", t().control], ["climate", t().climate]].map(([k, l]) => `<span><i style="background:${COLORS[k]}"></i>${l}</span>`).join("");
  const isReg = forestKind === "reg";
  const rows = isReg ? DATA.regresion : DATA.clasificacion;
  const [min, max, ref, d] = isReg ? [0.01, 0.04, DATA.ref_regresion, 4] : [0, 1, 0.5, 2];
  const bestValue = isReg ? Math.min(...rows.map((r) => r.v)) : Math.max(...rows.map((r) => r.v));
  const pos = (v) => (100 * (v - min)) / (max - min);
  el("forest").innerHTML = rows.map((r) => {
    const color = COLORS[r.rol];
    const ci = r.hi > r.lo ? ` (${dec(r.lo, d)}–${dec(r.hi, d)})` : "";
    const best = r.v === bestValue;
    return `<div class="frow${best ? " best-row" : ""}"><div class="fhead"><span>${r[lang]}${best ? `<span class="tag">· ${t().best}</span>` : ""}</span><b>${dec(r.v, d)}${ci}</b></div>
      <div class="track" aria-hidden="true"><span class="ref" style="left:${pos(ref)}%"></span><span class="ci" style="left:${pos(r.lo)}%;width:${pos(r.hi) - pos(r.lo)}%;background:${color}"></span><span class="dot" style="left:${pos(r.v)}%;background:${color}"></span></div></div>`;
  }).join("");
  el("forest-cap").textContent = isReg ? t().capReg : t().capCls;
}

/* Heatmap */
function divRgb(z) {
  const low = [11, 74, 117], mid = [243, 246, 248], high = [224, 113, 0];
  const a = Math.min(1, Math.abs(z) / 2.2);
  const end = z > 0 ? high : low;
  return mid.map((m, i) => Math.round(m + (end[i] - m) * a));
}
function inkOn(rgb) {
  const [r, g, b] = rgb.map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  const l = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return 1.05 / (l + 0.05) >= (l + 0.05) / 0.05 ? "#fff" : "#000";
}
function renderHeat() {
  tabsOf("heat-tabs", [["mort", t().mortality], ["ci", t().ci], ["precip", t().precip]], heatKind, (k) => { heatKind = k; heatCell = null; renderHeat(); });
  const set = DATA.anomalias[heatKind];
  let html = `<div></div>${DATA.anios.map((y) => `<div class="hd">’${String(y).slice(2)}</div>`).join("")}`;
  Object.entries(set.z).forEach(([dept, values]) => {
    const name = dept === "Média" ? t().mean : dept;
    html += `<div class="rw">${name}</div>`;
    values.forEach((z, i) => {
      const on = heatCell && heatCell[0] === dept && heatCell[1] === i;
      html += `<button type="button" class="${on ? "on" : ""}" data-d="${dept}" data-i="${i}" style="background:rgb(${divRgb(z).join(",")});color:${inkOn(divRgb(z))}" aria-label="${name} ${DATA.anios[i]}: ${dec(z, 1)}">${dec(z, 1)}</button>`;
    });
  });
  el("heat").innerHTML = html;
  el("heat").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { heatCell = [b.dataset.d, +b.dataset.i]; renderHeat(); }));
  if (heatCell) {
    const [dept, i] = heatCell;
    const name = dept === "Média" ? t().mean : dept;
    const raw = set.raw[dept][i], z = set.z[dept][i];
    el("heat-detail").textContent = `${name}, ${DATA.anios[i]}: ${dec(raw, set.dec)} ${t().heatUnit[heatKind]} (z = ${z > 0 ? "+" : ""}${dec(z, 1)})`;
  } else {
    el("heat-detail").textContent = t().tap;
  }
}

/* Líneas */
function renderChips() {
  const names = [null, ...DATA.departamentos.map((d) => d.nombre)];
  el("dept-chips").innerHTML = names.map((n) => `<button class="chip" type="button" data-dept="${n ?? ""}" aria-pressed="${n === deptSel}">${n ?? t().all}</button>`).join("");
  el("dept-chips").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { deptSel = b.dataset.dept || null; renderChips(); renderLine(); }));
}
function renderLine() {
  const W = 360, H = 230, L = 32, R = 18, T = 10, B = 26, yMin = 20, yMax = 120, years = DATA.anios;
  const x = (i) => L + (i * (W - L - R)) / (years.length - 1);
  const y = (v) => T + ((yMax - v) * (H - T - B)) / (yMax - yMin);
  const path = (vs) => vs.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)} ${y(v).toFixed(1)}`).join("");
  let s = "";
  [20, 40, 60, 80, 100, 120].forEach((k) => { s += `<line x1="${L}" x2="${W - R}" y1="${y(k)}" y2="${y(k)}" stroke="#e4eef5"/><text x="${L - 5}" y="${y(k) + 3.5}" text-anchor="end" font-size="10" font-family="Arial" fill="#52606d">${k}</text>`; });
  years.forEach((yr, i) => { if (i % 2 === 0) s += `<text x="${x(i)}" y="${H - 8}" text-anchor="middle" font-size="10" font-family="Arial" fill="#52606d">${yr}</text>`; });
  Object.entries(DATA.mortalidad).forEach(([name, vs]) => {
    const on = name === deptSel;
    s += `<path d="${path(vs)}" fill="none" stroke="${on ? "#d96f00" : "#a3c3da"}" stroke-width="${on ? 3.5 : 1.5}"/>`;
    if (on) vs.forEach((v, i) => { s += `<circle cx="${x(i)}" cy="${y(v)}" r="3.5" fill="#d96f00"><title>${years[i]}: ${dec(v, 1)}</title></circle>`; });
  });
  s += `<path d="${path(DATA.mortalidad_media)}" fill="none" stroke="#003255" stroke-width="3.5"/>`;
  DATA.mortalidad_media.forEach((v, i) => { s += `<circle cx="${x(i)}" cy="${y(v)}" r="3" fill="#003255"><title>${t().mean} ${years[i]}: ${dec(v, 1)}</title></circle>`; });
  el("linea").innerHTML = s;
}

/* Correlaciones */
function renderCorrelations() {
  const kinds = [["global", "#c9dde9", t().global], ["intra", "#1f6595", t().intra], ["intra_anio", "#d96f00", t().intraYear]];
  el("correlaciones").innerHTML = Object.entries(DATA.correlaciones).map(([key, v]) => `<div><div class="bar-title">${t().var[key]}</div>${kinds.map(([k, c, l]) => `<div class="bar"><span class="bar-label">${l}</span><i style="width:${(v[k] / 0.6) * 46}%;background:${c}"></i><span>${dec(v[k], 2)}</span></div>`).join("")}</div>`).join("");
}

/* Preguntas */
function renderFaqCats() {
  el("faq-cats").innerHTML = Object.entries(t().cats).map(([k, l]) => `<button class="chip" type="button" data-c="${k}" aria-pressed="${k === faqCat}">${l}</button>`).join("");
  el("faq-cats").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => { faqCat = b.dataset.c; renderFaqCats(); filterFaq(); }));
}
function normalize(s) { return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
function filterFaq() {
  let shown = 0;
  document.querySelectorAll("#faq details").forEach((d) => {
    const text = normalize([...d.querySelectorAll("." + lang)].map((n) => n.textContent).join(" "));
    const ok = (faqCat === "all" || d.dataset.cat === faqCat) && (!faqText || text.includes(faqText));
    d.hidden = !ok;
    if (ok) shown++;
  });
  el("faq-empty").hidden = shown > 0;
}

function renderAll() {
  renderPresets(); renderCalc(); renderDepts(); renderYears(); renderQuiz(); renderForest(); renderHeat();
  renderChips(); renderLine(); renderCorrelations(); renderFaqCats(); filterFaq();
}

/* Interacciones generales */
document.querySelectorAll("[data-set-lang]").forEach((b) => b.addEventListener("click", () => setLang(b.dataset.setLang)));
["ci-t", "ci-v", "ci-p"].forEach((id) => el(id).addEventListener("input", renderCalc));
["faq-search-es", "faq-search-pt"].forEach((id) => el(id).addEventListener("input", (e) => { faqText = normalize(e.target.value.trim()); filterFaq(); }));
el("share").addEventListener("click", async () => {
  const url = location.origin + location.pathname;
  if (navigator.share) { try { await navigator.share({ title: t().shareTitle, url }); } catch (e) { /* cancelado */ } return; }
  try { await navigator.clipboard.writeText(url); } catch (e) { /* sin portapapeles */ }
  const toast = el("toast");
  toast.textContent = t().copied;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1800);
});
addEventListener("scroll", () => {
  const max = document.documentElement.scrollHeight - innerHeight;
  el("progress").style.width = (max > 0 ? (100 * scrollY) / max : 0) + "%";
}, { passive: true });

drawGauge();
setLang(pickLang());

if ("IntersectionObserver" in window) {
  const revealer = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("in"); revealer.unobserve(e.target); }
  }), { rootMargin: "0px 0px -6% 0px" });
  document.querySelectorAll(".reveal").forEach((n) => revealer.observe(n));
  const tabs = document.querySelectorAll("[data-spy]");
  const spy = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (!e.isIntersecting) return;
    tabs.forEach((a) => {
      const on = a.dataset.spy === e.target.id;
      a.classList.toggle("on", on);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }), { rootMargin: "-45% 0px -50% 0px" });
  ["inicio", "chill", "metodo", "resultados", "faq"].forEach((id) => spy.observe(el(id)));
  const yearObserver = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting && !yearTimer && !reduced()) {
      yearTimer = setInterval(() => { yearSel = (yearSel + 1) % DATA.anios.length; renderYears(); }, 2400);
    } else if (!e.isIntersecting && yearTimer) { clearInterval(yearTimer); yearTimer = null; }
  }));
  yearObserver.observe(el("years"));
} else {
  document.querySelectorAll(".reveal").forEach((n) => n.classList.add("in"));
}
</script>
</body>
</html>
