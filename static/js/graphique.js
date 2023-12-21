
<script>
    document.addEventListener("DOMContentLoaded", function () {
        if ($('#sales_chartss').length > 0) {
            var options = {
                series: [
                    { name: 'Recettes', data: [{{ total_revenue|default:0 }}, {{ monthly_revenue|default:0 }}] },
                    { name: 'Dépenses', data: [{{ total_total_expenses|default:0 }}, {{ monthly_total_expenses|default:0 }}] }
                ],
                colors: ['#28C76F', '#EA5455'],
                chart: { type: 'bar', height: 300, stacked: true, zoom: { enabled: true } },
                responsive: [{ breakpoint: 280, options: { legend: { position: 'bottom', offsetY: 0 } } }],
                plotOptions: { bar: { horizontal: false, columnWidth: '20%', endingShape: 'rounded' } },
                xaxis: { categories: ['Total', 'Mois en cours'] },
                legend: { position: 'right', offsetY: 40 },
                fill: { opacity: 1 }
            };

            var chart = new ApexCharts(document.querySelector("#sales_chartss"), options);
            chart.render();
        }
    });
</script>