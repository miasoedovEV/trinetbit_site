const lang_page = document.getElementsByClassName('info_lan')[0].value
console.log(lang_page)

if (lang_page == "en") {
    var name_time = "Время в месяцах";
    var name_depo = "Стартовый депозит";
    var name_profit = "Ваша прибыль";
} else {
    var name_time = 'time (monthly)';
    var name_depo = 'Initial deposit';
    var name_profit = 'Your profit';
}

function getProfit()  {
    let start_depo = document.getElementById('start_depo');
        time_month = document.getElementById('time_month');
        profit = document.getElementById('profit');
    if (time_month.value != name_time && start_depo.value != name_depo) {
        let profit_month = 0
            month = Number(time_month.value)
            start_depo_value = Number(start_depo.value)
            depo = Number(start_depo.value)
        for (let i = 0; i < month; i++) {
            depo = depo * 1.125
            }
        profit.value = Math.round((depo - start_depo_value) * 100) / 100
    }
    if (profit.value == "0" || profit.value == "0") {
        profit.value = name_profit;
    }
}

setInterval(getProfit, 2000);