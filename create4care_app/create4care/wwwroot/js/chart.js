// wwwroot/js/home‐chart.js
window.createHomeChart = () => {
  const ctx = document.getElementById('myChart');
  if (!ctx) return;

  const labels = ['Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7'];
  const data = {
    labels,
    datasets: [{
      label: 'Measurement',
      data: [130,133,137,142,145,148,150],
      fill: true,
      borderColor: 'rgb(75,192,192)',
      backgroundColor: 'rgba(75,192,192,0.2)',
      tension: 0.1
    }]
  };
  const config = {
    type: 'line',
    data,
    options: {
      scales: {
        y: {
          min: 130,
          max: 150,
          ticks: { stepSize: 1, callback: v => v + ' cm' },
          title: { display: true, text: 'Height (cm)' }
        },
        x: { title: { display: true, text: 'Week' } }
      },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => ctx.parsed.y + ' cm' } }
      }
    }
  };
  new Chart(ctx, config);
};
