$(function (){
    initPie_income();
    initLine_entrepre_num();
    initHistogram_edu();
    initBar_famtype();
})

// {# 图表1：收入情况 饼图 #}
function initPie_income(){
    var myChart = echarts.init(document.getElementById('char1'));

    var option = {
        tooltip : {
            trigger: 'item',
            formatter: "{b} : {c} <br/>({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : 'left',
            textStyle : {
                color : '#ffffff',
                fontSize : 10
            },
            data:[]
         },

        calculable : false,
        series : [
            {
                name:'收入情况',
                type:'pie',
                radius : ['40%', '70%'],
                itemStyle : {
                    normal : {
                        label : {
                            show : false
                        },
                        labelLine : {
                            show : false
                        }
                    },
                    emphasis : {
                        label : {
                            show : true,
                            position : 'center',
                            textStyle : {
                                fontSize : '20',
                                fontWeight : 'bold'
                            }
                        }
                    }
                },
                data:[]
            }
        ]
    };

    $.ajax({
        url: "/chart_1/",
        type: "get",
        dataType: "JSON",
        success: function (res){
            // 将后台返回的数据更新到option中
            if(res.status){
                option.legend.data = res.legend;
                option.series[0].data = res.db_data_list;
                // 使用指定的配置项展示图表
                myChart.setOption(option);
            }
            else {
                alert("“家庭收入水平”数据获取失败！")
            }
        }
    })
    window.addEventListener('resize', function () {myChart.resize();})
}

// {# 图表2：创业人数随时间变化 折线图 #}
function  initLine_entrepre_num(){
    var myChart = echarts.init(document.getElementById('char2'));

    var option = {
        legend: {
            data:[],
            textStyle : {
                color : '#ffffff',

            }
        },
        grid: {show:'true',borderWidth:'0'},

        calculable : false,
        tooltip : {
            trigger: 'axis',
        },
        xAxis : [
            {
                type : 'category',
                axisLabel : {
                    textStyle: {
                        color: '#fff'
                    }
                },

                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                },

                data: []
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLine : {onZero: false},
                axisLabel : {
                    textStyle: {
                        color: '#fff'
                    }
                },
                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                },
                boundaryGap : false,
                min: 100,
                max: 250,

                // {#data : [150, 200, 250, 300, 350]#}
            }
        ],
        series : [
            {
                name:'创业人数',
                type:'line',
                smooth:false,
                itemStyle: {
                    normal: {
                        lineStyle: {
                            shadowColor : 'rgba(0,0,0,0.4)'
                        }
                    }
                },
                data:[]
            }
        ]
    };

    $.ajax({
        url: "/chart_2/",
        type: "get",
        dataType: "JSON",
        success: function (res){
            // 将后台返回的数据更新到option中
            if(res.status){
                option.legend.data = res.legend;
                option.xAxis[0].data = res.x_axis;
                option.series[0].data = res.data;
                // 使用指定的配置项展示图表
                myChart.setOption(option);
            }
            else {
                alert("”创业与家庭类型“数据获取失败！")
            }
        }
    })
    window.addEventListener('resize', function () {myChart.resize();})
}

// {# 图表3：受教育程度和创业的关系 堆叠条形图 #}
function initHistogram_edu(){
    var myChart = echarts.init(document.getElementById('char3'));

    var option = {
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {show:'true',borderWidth:'0'},
        legend: {
            data:[],
            textStyle : {
                color : '#ffffff',

            }
        },

        calculable :false,
        xAxis : [
            {
                type : 'value',
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff'
                    }
                },
                splitLine:{
                    lineStyle:{
                        color:['#f2f2f2'],
                        width:0,
                        type:'solid'
                    }
                }

            }
        ],
        yAxis : [
            {
                type : 'category',
                data : [],
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff'
                    }
                },
                splitLine:{
                    lineStyle:{
                        width:0,
                        type:'solid'
                    }
                }
            }
        ],
        series : []
    };

    $.ajax({
        url: "/chart_3/",
        type: "get",
        dataType: "JSON",
        success: function (res){
            // 将后台返回的数据更新到option中
            if(res.status){
                option.legend.data = res.legend;
                option.yAxis[0].data = res.y_axis;
                option.series = res.series_list;
                // 使用指定的配置项展示图表
                myChart.setOption(option);
            }
            else {
                alert("”受教育程度和创业的关系“数据获取失败！")
            }
        }
    })

    window.addEventListener('resize', function () {myChart.resize();})

}

// {# 图表4：家庭类型-是否创业 柱形图 #}
function initBar_famtype(){
    var myChart = echarts.init(document.getElementById('char4'));

    var option = {
        grid: {show:'true',borderWidth:'0'},
        legend: {
            data: [],
            textStyle : {
                color : '#ffffff',
                }
            },
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
        },

        xAxis : [
            {
                type : 'category',
                splitLine: {show:false},
                data : [],
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff'
                    }
                }

            }
        ],
        yAxis : [
            {
                type : 'value',
                splitLine: {show:false},
                axisLabel: {
                    show: true,
                    textStyle: {
                        color: '#fff'
                    }
                }
            }
        ],
        series : []
    };

    $.ajax({
        url: "/chart_4/",
        type: "get",
        dataType: "JSON",
        success: function (res){
            // 将后台返回的数据更新到option中
            if(res.status){
                option.legend.data = res.legend;
                option.xAxis[0].data = res.x_axis;
                option.series = res.series_list;
                // 使用指定的配置项展示图表
                myChart.setOption(option);
            }
            else {
                alert("”创业与家庭类型“数据获取失败！")
            }
        }
    })

    window.addEventListener('resize', function () {myChart.resize();})
}