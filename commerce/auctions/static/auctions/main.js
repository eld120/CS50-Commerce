const btn = document.getquerySelector('#id_active')

btn.onclick = function () {
    const form = document.querySelector('#watchSubmit')
    form.requestSubmit()
}