function init(locale, currency, parameters) {
    const colors = [
        "#0074D9", "#FF4136", "#2ECC40", "#FF851B",
        "#7FDBFF", "#B10DC9", "#FFDC00", "#001f3f",
        "#39CCCC", "#01FF70", "#85144b", "#F012BE",
        "#3D9970", "#111111", "#AAAAAA"
    ];

    const ccyFormatter = new Intl.NumberFormat(locale, {style: 'currency', currency: currency});

    function getConfig(allocationBy, tickerToVolume) {
        const totalBalance = Object.values(tickerToVolume).reduce((a, b) => a + b, 0);

        function toLabels(tickerToVolume) {
            return Object.entries(tickerToVolume)
                .map((arr) => arr[0] + ' - ' + ccyFormatter.format(arr[1])
                    + ' (' + Math.round(arr[1] / totalBalance * 1000) / 10 + '%)');
        }

        return {
            type: 'pie',
            data: {
                labels: toLabels(tickerToVolume),
                datasets: [{
                    backgroundColor: colors,
                    borderColor: colors,
                    data: Object.values(tickerToVolume),
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: ['Allocation by ' + allocationBy, ccyFormatter.format(totalBalance)],
                        fullSize: true,
                        font: {
                            size: 20
                        }
                    },
                    legend: {
                        position: "right",
                        maxWidth: 300
                    },
                    tooltip: true,
                }
            }
        };
    }

    function getAllocs(aggregationKey, parameters) {
        const allocs = {};
        parameters.forEach(p => {
            let aggregationValue = p[aggregationKey];
            if (aggregationValue == null) {
                aggregationValue = {}
            } else if (typeof aggregationValue !== 'object') {
                aggregationValue = {[aggregationValue]: 1}
            }
            Object.entries(aggregationValue).forEach(entry => {
                const key = entry[0];
                const share = entry[1];
                const existingValue = allocs[key];
                allocs[key] = p.quantity * share + (existingValue == null ? 0 : existingValue);
            });
        });
        return Object.fromEntries(Object.entries(allocs).sort(([,a],[,b]) => b-a)); // sorting
    }

    const allocationBySelect = document.getElementById("allocationBy")
    Object.keys(parameters[0]).forEach(k => {
        const elem = document.createElement("option");
        elem.value = k;
        elem.innerHTML = k;
        allocationBySelect.appendChild(elem);
    });
    const chart = new Chart(document.getElementById("chart"),
        getConfig(allocationBySelect.value, getAllocs(allocationBySelect.value, parameters)));

    allocationBySelect.addEventListener("change", () => {
        const config = getConfig(allocationBySelect.value, getAllocs(allocationBySelect.value, parameters));
        chart.data = config.data;
        chart.options.plugins.title.text = config.options.plugins.title.text;
        chart.update();
    });
}
