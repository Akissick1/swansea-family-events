    stage:function(u){return sky(u,"#1A0B12","#2C0F1C","#3D1424")+
      '<path d="M200 150 L118 470 H282 Z" fill="#FFE3A8" opacity=".16"/>'+
      '<ellipse cx="200" cy="470" rx="96" ry="16" fill="#FFE3A8" opacity=".28"/>'+
      '<rect y="470" width="400" height="130" fill="#140910"/><rect y="466" width="400" height="8" fill="#5A2A1C"/>'+
      '<path d="M0 120 C30 220 26 380 60 470 H0Z" fill="#8E1F2F"/><path d="M0 120 C18 230 10 380 30 470 H0Z" fill="#6B1522"/>'+
      '<path d="M400 120 C370 220 374 380 340 470 H400Z" fill="#8E1F2F"/><path d="M400 120 C382 230 390 380 370 470 H400Z" fill="#6B1522"/>'+
      '<path d="M0 110 H400 V150 C340 170 300 150 260 165 C230 176 170 176 140 165 C100 150 60 170 0 150Z" fill="#A3283A"/>'+
      '<g fill="#0B0508"><circle cx="200" cy="370" r="15"/><path d="M186 388 h28 l10 82 h-48z"/><path d="M214 392 l30 -30 6 6 -30 34z"/></g>'+
      '<g fill="#F2C76B" opacity=".9"><circle cx="70" cy="132" r="4"/><circle cx="130" cy="140" r="4"/><circle cx="270" cy="140" r="4"/><circle cx="330" cy="132" r="4"/></g>';},
    mic:function(u){return sky(u,"#120E16","#1F1726","#2B1F33")+
      '<g fill="#3A2630" opacity=".55">'+
        [0,1,2,3,4,5,6,7,8,9,10,11].map(function(r){ var y=150+r*26, o=(r%2)*30; var s=''; for(var x=-30+o;x<420;x+=60) s+='<rect x="'+x+'" y="'+y+'" width="56" height="22" rx="2"/>'; return s; }).join("")+
      '</g>'+
      '<circle cx="200" cy="300" r="120" fill="#FFD98A" opacity=".18"/>'+
      '<circle cx="200" cy="300" r="70" fill="#FFD98A" opacity=".16"/>'+
      '<rect y="460" width="400" height="140" fill="#0D0A10"/><rect y="456" width="400" height="8" fill="#4A3340"/>'+
      '<g fill="#0B080C"><rect x="196" y="300" width="8" height="160"/><ellipse cx="200" cy="462" rx="34" ry="7"/>'+
        '<rect x="186" y="256" width="28" height="46" rx="14"/><rect x="194" y="300" width="12" height="8"/></g>'+
      '<g fill="#6E6A72"><rect x="190" y="262" width="20" height="3" rx="1.5"/><rect x="190" y="270" width="20" height="3" rx="1.5"/><rect x="190" y="278" width="20" height="3" rx="1.5"/></g>'+
      '<path d="M120 150 h160" stroke="#FF6A8A" stroke-width="6" stroke-linecap="round" opacity=".7" class="a-flick"/>';},
    gig:function(u){return sky(u,"#07071A","#1A0B3A","#3A0F4E")+
      '<g class="a-sway" opacity=".55">'+
        '<path d="M60 120 L10 470 H120Z" fill="#5BD1FF" opacity=".28"/>'+
        '<path d="M200 110 L140 470 H260Z" fill="#FF5FA2" opacity=".28"/>'+
        '<path d="M340 120 L280 470 H390Z" fill="#B8FF5B" opacity=".24"/></g>'+
      '<g fill="#F2F2FF"><circle cx="60" cy="118" r="7"/><circle cx="200" cy="108" r="7"/><circle cx="340" cy="118" r="7"/></g>'+
      '<rect y="96" width="400" height="10" fill="#14122A"/>'+
      '<g fill="#0A0814"><rect x="150" y="330" width="100" height="60" rx="4"/><circle cx="200" cy="300" r="14"/><path d="M184 316 h32 l8 60 h-48z"/>'+
        '<path d="M170 350 l70 -26 4 10 -70 26z"/></g>'+
      '<path d="M0 600 V470 '+
        [0,1,2,3,4,5,6,7,8,9].map(function(i){ var x=i*44; return 'Q'+(x+11)+' 432 '+(x+22)+' 452 L'+(x+26)+' 400 L'+(x+30)+' 452 Q'+(x+38)+' 440 '+(x+44)+' 466'; }).join(" ")+
        ' V600Z" fill="#05040C"/>';},
    stadium:function(u){return sky(u,"#0A1428","#13264A","#1F3C6A")+ stars()+
      '<g fill="#E9F2FF"><rect x="44" y="120" width="44" height="22" rx="3"/><rect x="312" y="120" width="44" height="22" rx="3"/></g>'+
      '<g fill="#0B1424"><rect x="63" y="142" width="6" height="250"/><rect x="331" y="142" width="6" height="250"/></g>'+
      '<path d="M66 140 L-40 470 H200Z" fill="#E9F2FF" opacity=".10"/><path d="M334 140 L440 470 H200Z" fill="#E9F2FF" opacity=".10"/>'+
      '<path d="M0 300 C120 270 280 270 400 300 V392 H0Z" fill="#162238"/>'+
      '<g fill="#22324F">'+[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19].map(function(i){ return '<circle cx="'+(10+i*20)+'" cy="'+(318+(i%3)*8)+'" r="5"/><circle cx="'+(20+i*20)+'" cy="'+(346+(i%2)*8)+'" r="5"/>'; }).join("")+'</g>'+
      '<path d="M0 392 H400 V600 H0Z" fill="#1E6B3A"/><path d="M0 392 H400 V410 H0Z" fill="#23803F"/>'+
      '<g stroke="#E9F2FF" stroke-width="3" fill="none" opacity=".8"><path d="M30 600 L80 420 H320 L370 600"/><path d="M200 420 V600"/><ellipse cx="200" cy="500" rx="54" ry="22"/></g>';},
    paint:function(u){return sky(u,"#2A1E2E","#4A2E3C","#7A4A48")+
      '<circle cx="320" cy="170" r="60" fill="#FFCF8A" opacity=".18"/>'+
      '<rect y="470" width="400" height="130" fill="#24161C"/><rect y="466" width="400" height="8" fill="#5C3A34"/>'+
      '<g stroke="#2A170F" stroke-width="10" stroke-linecap="round"><path d="M150 470 L196 170"/><path d="M262 470 L214 170"/><path d="M205 200 L205 470"/></g>'+
      '<rect x="120" y="190" width="170" height="200" rx="4" fill="#F7F1E6"/>'+
      '<path d="M132 360 C170 300 200 340 230 290 C250 260 270 300 280 280 V380 H132Z" fill="#3E8E7E"/>'+
      '<circle cx="250" cy="236" r="22" fill="#F2B33D"/><path d="M132 300 C160 270 190 290 210 260" stroke="#E0554A" stroke-width="10" fill="none" stroke-linecap="round"/>'+
      '<rect x="114" y="384" width="182" height="12" rx="3" fill="#3A2216"/>'+
      '<g transform="translate(330 400)"><path d="M-16 0 C-16 34 16 34 16 0Z" fill="#C2405A" opacity=".85"/><path d="M-18 -2 H18" stroke="#F7F1E6" stroke-width="3"/><rect x="-2" y="30" width="4" height="34" fill="#F7F1E6"/><rect x="-14" y="62" width="28" height="4" rx="2" fill="#F7F1E6"/></g>'+
      '<g transform="translate(70 420) rotate(-20)"><ellipse rx="40" ry="26" fill="#E8D7BF"/><circle cx="-16" cy="-6" r="6" fill="#E0554A"/><circle cx="2" cy="-12" r="6" fill="#4FA9C9"/><circle cx="18" cy="-2" r="6" fill="#F2B33D"/><circle cx="-2" cy="8" r="6" fill="#8FC46B"/></g>';},
    nightout:function(u){return sky(u,"#0B0716","#1C0E33","#3A1250")+ stars()+
      '<g class="a-flick"><circle cx="200" cy="170" r="44" fill="#C9D3E8"/>'+
        '<g fill="#8A97B5">'+[0,1,2,3,4,5].map(function(r){ var s=''; for(var c=0;c<6;c++) if((r+c)%2) s+='<rect x="'+(160+c*14)+'" y="'+(130+r*14)+'" width="12" height="12"/>'; return s; }).join("")+'</g></g>'+
      '<path d="M200 96 V126" stroke="#C9D3E8" stroke-width="3"/>'+
      '<g opacity=".5"><path d="M200 170 L40 420" stroke="#FF5FA2" stroke-width="5"/><path d="M200 170 L360 400" stroke="#5BD1FF" stroke-width="5"/><path d="M200 170 L120 460" stroke="#F2E35B" stroke-width="4"/><path d="M200 170 L300 470" stroke="#B8FF5B" stroke-width="4"/></g>'+
      '<path d="M0 600 V420 H40 V380 H90 V430 H130 V360 H180 V440 H220 V390 H270 V430 H310 V370 H360 V420 H400 V600Z" fill="#07050E"/>'+
      '<g fill="#FFD27A" opacity=".8"><rect x="54" y="396" width="8" height="10"/><rect x="146" y="380" width="8" height="10"/><rect x="236" y="404" width="8" height="10"/><rect x="326" y="386" width="8" height="10"/><rect x="160" y="404" width="8" height="10"/></g>'+
      '<g transform="translate(300 520)"><path d="M-20 -30 L20 -30 L0 0Z" fill="#FF5FA2" opacity=".85"/><rect x="-2" y="0" width="4" height="30" fill="#E9E2F5"/><rect x="-14" y="28" width="28" height="4" rx="2" fill="#E9E2F5"/></g>'+
      '<g transform="translate(100 520)"><path d="M-20 -30 L20 -30 L0 0Z" fill="#5BD1FF" opacity=".85"/><rect x="-2" y="0" width="4" height="30" fill="#E9E2F5"/><rect x="-14" y="28" width="28" height="4" rx="2" fill="#E9E2F5"/></g>';},
    talk:function(u){return sky(u,"#0E1A22","#173040","#21485A")+
      '<rect x="60" y="150" width="280" height="170" rx="6" fill="#0B141B"/><rect x="70" y="160" width="260" height="150" rx="3" fill="#2E6F86"/>'+
      '<path d="M70 280 L150 220 L200 256 L262 196 L330 250 V310 H70Z" fill="#1E4E60"/><circle cx="290" cy="196" r="16" fill="#F2C76B"/>'+
      '<circle cx="200" cy="360" r="90" fill="#FFE3A8" opacity=".14"/>'+
      '<rect y="470" width="400" height="130" fill="#0A1218"/><rect y="466" width="400" height="8" fill="#38505C"/>'+
      '<g fill="#081016"><circle cx="146" cy="352" r="13"/><path d="M134 368 h24 l8 102 h-40z"/></g>'+
      '<g fill="#14232C"><path d="M220 380 H300 L292 470 H228Z"/><rect x="214" y="370" width="92" height="14" rx="3"/></g>'+
      '<rect x="252" y="350" width="4" height="22" fill="#14232C"/><circle cx="254" cy="348" r="5" fill="#14232C"/>';},
    dine:function(u){return sky(u,"#1E1410","#3A2418","#5A3420")+
      '<g fill="#FFD27A" opacity=".85">'+[60,120,180,240,300,350].map(function(x,i){ return '<circle class="a-flick" style="animation-delay:'+(i*0.3)+'s" cx="'+x+'" cy="'+(120+(i%2)*14)+'" r="4"/>'; }).join("")+'</g>'+
      '<path d="M20 116 Q200 150 380 116" stroke="#2A1A10" stroke-width="2" fill="none"/>'+
      '<rect y="380" width="400" height="220" fill="#2A170E"/><path d="M0 380 H400 V398 H0Z" fill="#6B3E22"/>'+
      '<ellipse cx="200" cy="430" rx="170" ry="34" fill="#F3E9D8"/><ellipse cx="200" cy="430" rx="150" ry="26" fill="#FBF5EA"/>'+
      '<ellipse cx="130" cy="428" rx="40" ry="10" fill="#E8DCC6"/><ellipse cx="270" cy="428" rx="40" ry="10" fill="#E8DCC6"/>'+
      '<circle cx="130" cy="424" r="14" fill="#C2405A" opacity=".85"/><circle cx="270" cy="424" r="14" fill="#8FC46B" opacity=".9"/>'+
      '<g transform="translate(200 360)"><rect x="-6" y="0" width="12" height="60" rx="3" fill="#F7F1E6"/><path class="a-flick" d="M0 -26 C10 -12 8 -4 0 0 C-8 -4 -10 -12 0 -26Z" fill="#FFC86B"/><circle cy="-12" r="40" fill="#FFC86B" opacity=".18"/></g>'+
      '<g transform="translate(90 360)"><path d="M-14 0 C-14 26 14 26 14 0Z" fill="#8E1F2F" opacity=".9"/><path d="M-16 -2 H16" stroke="#F7F1E6" stroke-width="2.5"/><rect x="-2" y="24" width="4" height="34" fill="#F7F1E6"/><rect x="-12" y="56" width="24" height="4" rx="2" fill="#F7F1E6"/></g>'+
      '<g transform="translate(310 360)"><path d="M-14 0 C-14 26 14 26 14 0Z" fill="#F2D17A" opacity=".85"/><path d="M-16 -2 H16" stroke="#F7F1E6" stroke-width="2.5"/><rect x="-2" y="24" width="4" height="34" fill="#F7F1E6"/><rect x="-12" y="56" width="24" height="4" rx="2" fill="#F7F1E6"/></g>';},
    mystery:function(u){return sky(u,"#0C1612","#13241C","#1C3428")+
      '<g fill="#22382C" opacity=".7">'+[0,1,2,3,4,5,6].map(function(i){ return '<rect x="'+(i*60-10)+'" y="110" width="44" height="330" rx="3"/>'; }).join("")+'</g>'+
      '<circle cx="200" cy="300" r="130" fill="#FFD27A" opacity=".10"/>'+
      '<rect y="440" width="400" height="160" fill="#0A100D"/><rect y="436" width="400" height="8" fill="#4A3424"/>'+
      '<g transform="translate(110 360)"><rect x="-5" y="0" width="10" height="76" fill="#E9E2D0"/><path class="a-flick" d="M0 -26 C9 -12 7 -4 0 0 C-7 -4 -9 -12 0 -26Z" fill="#FFC86B"/><circle cy="-10" r="34" fill="#FFC86B" opacity=".2"/></g>'+
      '<g transform="translate(250 330) rotate(-25)"><circle r="42" fill="none" stroke="#C9A55A" stroke-width="10"/><circle r="36" fill="#9FD3C7" opacity=".18"/><rect x="34" y="-7" width="70" height="14" rx="7" fill="#5A3A22"/></g>'+
      '<g transform="translate(190 432) rotate(8)"><path d="M0 0 L70 -6 L74 0 L70 6Z" fill="#C8CED6"/><rect x="-26" y="-6" width="28" height="12" rx="4" fill="#5A1E24"/><rect x="-4" y="-14" width="6" height="28" rx="2" fill="#C9A55A"/></g>'+
      '<text x="320" y="230" text-anchor="middle" font-family="Georgia,serif" font-size="120" fill="#C2405A" opacity=".75" class="a-flick">?</text>';},
