var is_checked = document.getElementById('result-message').getAttribute('data-jsone')

if (is_checked == "Checked") {
    const div_result_message = document.getElementById('result-message')
    const window_done = document.getElementById('done')
    const window_example = document.getElementById('exampleModal')
    const window_example2 = document.getElementById('exampleModal2')
    const body = document.getElementsByTagName('body')[0]
    window_done.style.display = "block"
    window_done.className = "modal fade show"
    body.style['overflow'] = "hidden"
    body.style['padding-right'] = "16px"
    window_example.style['display'] = "none"
    window_example2.style['display'] = "none"
    let div_drop = document.createElement('div');
        div_drop.className = "modal-backdrop fade show";
        document.body.append(div_drop);
    window_done.addEventListener('click', function (event) {
        window_done.style.display = "none"
        window_done.className = "modal fade"
        body.style = ""
        div_drop.remove()
        div_result_message.textContent = "Data is checked!"
    });
  }

    
