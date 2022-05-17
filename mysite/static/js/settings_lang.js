const btnradio1 = document.getElementById('btnradio1')
const btnradio3 = document.getElementById('btnradio3')
const lang = document.getElementsByClassName('info_lan')[0].value

if (lang == "ru") {
    btnradio1.type = 'submit'
    btnradio3.type = 'radio'
    btnradio3.checked = true
  } else {
    btnradio1.type = 'radio'
    btnradio3.type = 'submit'
  } 


    
