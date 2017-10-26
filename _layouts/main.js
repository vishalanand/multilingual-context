<script type="text/javascript" src="http://echarts.baidu.com/gallery/vendors/echarts/echarts-all-3.js"></script>
       <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
       <script type="text/javascript">

        var dom = document.getElementById("container");
        var myChart = echarts.init(dom);
        var app = {};
        option = null;
        var key = "1ndNXEMrekWBqraIInvAXW27RIXtkdlXiWoW7IhM_QaM";
        var url = "https://spreadsheets.google.com/feeds/list/" + key + "/od6/public/values?alt=json";

        var obj1 = {}
        $.get(url, function (result) {
            var data = [];
            $(result.feed.entry).each(function (index, row) {
                if (obj1[row.gsx$language.$t] == undefined) {
                    obj1[row.gsx$language.$t] = []

                }
                obj1[row.gsx$language.$t].push([row.gsx$x.$t, row.gsx$y.$t, 0.2, row.gsx$word.$t, row.gsx$language.$t])
            });
            var series1 = []
            var legend1 = []
            for(var className in obj1) {
                legend1.push(className);
                series1.push({
                    name: className,
                    type: 'scatter',
                    data: obj1[className],
                    itemStyle: {
                            normal: {
                                opacity: 0.8
                            }
                        },
                    symbolSize: function (val) {
                        return val[2] * 40;
                    }
                });
            }
            option = {
                animation: true,
                legend: {
                    data: legend1,
                    type: "scroll"
                },
                tooltip: {
                },
                xAxis: {
                    type: 'value',
                    //min: 'dataMin',
                    //max: 'dataMax',
                    splitLine: {
                        show: true
                    }
                },
                yAxis: {
                    type: 'value',
                    //min: 'dataMin',
                    //max: 'dataMax',
                    splitLine: {
                        show: true
                    }
                },
                dataZoom: [
                    {
                        type: 'slider',show: true,xAxisIndex: [0]
                    },
                    {
                        type: 'slider',show: true,yAxisIndex: [0],left: '93%'
                    },
                    {
                        type: 'inside',
                        xAxisIndex: [0]//,start: 1,end: 35
                    },
                    {
                        type: 'inside',
                        yAxisIndex: [0]//,start: 29,end: 36
                    }
                ],
                series: series1
            };
            if (option && typeof option === "object") {
                myChart.setOption(option, true);
            }
        });
       </script>