//Graph 01
var ctx = document.getElementById("canvas").getContext("2d");
var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: labelsAdjusted,
    datasets: [
      {
        label: "Temperature",
        data: Ylabels,
        backgroundColor: "#b3e2eb",
        borderColor: "#0046FE",
        borderWidth: 3,
        tension: 0.4,
        fill: true,
        radius: 0,
        hoverRadius: 7,
      },
    ],
  },
  options: {
    plugins: {
      legend: {
        // labels: {
        //   boxWidth: 0,
        // },
      },

      tooltip: {
        titleColor: "#000",
        titleAlign: 'center' ,
        titleSpacing: 0 ,
        titleFont: {
          size: 12
        },

        

        backgroundColor: '#b3e2eb',
        borderWidth: 3,
        padding: 10,
        cornerRadius: 10,
        borderColor: "#0046FE",


        bodyColor: "#000" ,
        bodyAlign: 'center',
        bodyFont: {
          size: 20,
          weight: 'bold',
        },

        displayColors: false,
      
        callbacks: {
          title: (context) => {
            
            return context[0].label.replaceAll(',', ' ');
          },

          beforeTitle: function(context){
            return "Graph"
          },

          // label: function(tooltipItems, data) { 
          //   console.log(tooltipItems);
          //   console.log(tooltipItems.dataset.label);
          //   // console.log(tooltipItems.dataset.data.map((value) => value))
            
          //   return tooltipItems + '°C';
          // }
        },
      },
    },

    
    hover: {
      mode: "index",
      intersect: false,
    },
    maintainAspectRatio: false,
    elements: {},
    scales: {
      x: {
        ticks: {
          maxTicksLimit: 10,
          font: {
            size: 9,
          },
        },
        display: true,
        grid: {
          display: false,
        },
      },
      y: {
        display: true,
        beginAtZero: true,
        grid: {
          display: false,
        },
      },
    },
  },
});














