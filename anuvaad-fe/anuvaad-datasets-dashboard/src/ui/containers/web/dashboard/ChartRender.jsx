import React from "react";
import { withRouter } from "react-router-dom";
import { withStyles } from '@material-ui/core/styles';

import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import Toolbar from "@material-ui/core/Toolbar";
import AppBar from "@material-ui/core/AppBar";
import Typography from "@material-ui/core/Typography";
import MenuIcon from '@material-ui/icons/Menu';
import BackIcon from '@material-ui/icons/ArrowBack';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import GlobalStyles from "../../../styles/web/styles";
import Theme from "../../../theme/web/theme-red";

import classNames from "classnames";
import history from "../../../../web.history";
import {
  BarChart, Bar, Brush, Cell, CartesianGrid, ReferenceLine, ReferenceArea,
  XAxis, YAxis, Tooltip, Legend, ErrorBar, LabelList, Rectangle, Surface,
  Symbols
} from 'recharts';
import ReactECharts from 'echarts-for-react';
import _ from 'lodash';

import APITransport from "../../../../flux/actions/apitransport/apitransport";
import { showSidebar } from '../../../../flux/actions/apis/common/showSidebar';

var randomColor = require('randomcolor');
var jp = require('jsonpath')
const data = [
  {
    "updatedTimestamp": "2021-02-25T00:00:00.000Z",
    "version": "2021-v1",
    "src_name": "PIB",
    "domain": "General",
    "languagePair": "en-hi",
    "site": "pib.gov.in",
    "count": 401859,
    "pair-type": "Machine Readable"
  },
  {
    "updatedTimestamp": "2021-02-25T00:00:00.000Z",
    "version": "2021-v1",
    "src_name": "PIB",
    "domain": "General",
    "languagePair": "en-bn",
    "site": "pib.gov.in",
    "count": 74433,
    "pair-type": "Machine Readable"
  },
  {
    "updatedTimestamp": "2021-02-25T00:00:00.000Z",
    "version": "2021-v1",
    "src_name": "PIB",
    "domain": "General",
    "languagePair": "en-ta",
    "site": "pib.gov.in",
    "count": 104836,
    "pair-type": "Machine Readable"
  },
  {
    "updatedTimestamp": "2021-02-25T00:00:00.000Z",
    "version": "2021-v1",
    "src_name": "PIB",
    "domain": "General",
    "languagePair": "en-te",
    "site": "pib.gov.in",
    "count": 65842,
    "pair-type": "Machine Readable"
  },
  {
    "updatedTimestamp": "2021-02-25T00:00:00.000Z",
    "version": "2021-v1",
    "src_name": "PIB",
    "domain": "General",
    "languagePair": "en-ml",
    "site": "pib.gov.in",
    "count": 27538,
    "pair-type": "Machine Readable"
  }

];
const data1 = [
  { value: 100, label: 'Hindi' },
  { value: 260, label: 'English' },
  { value: 200, label: 'Tamil' },
  { value: 400, label: 'Malayalam' },
  { value: 300, label: 'Kannnada' },
  { value: 200, label: 'Bengali' },
  { value: 600, label: 'Marati' },
  { value: 30, label: 'Telugu' },
  { value: 200, label: 'Punjabi' },
  { value: 500, label: 'Assamese' },
  { value: 410, label: 'Nepali' },
  { value: 300, label: 'Gujarati' },
  { value: 200, label: 'Punjabi' },
  { value: 250, label: 'Malayalam' },
  { value: 100, label: 'Kannnada' },
  { value: 357, label: 'Telugu' },
  { value: 230, label: 'Punjabi' },
  { value: 200, label: 'Hindi' },
  { value: 200, label: 'English' },
  { value: 99, label: 'Kannnada' },
  { value: 555, label: 'Telugu' },
]
class ChartRender extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      word: "",
      chartColors: {
        others: "#40ee86",
        meat: "#67d6c0",
        pasta: "#127197",
        pizza: "#e96d8d"
      },
    }

  }

  getData(dataValue) {
    let condition = `$..[*].${dataValue}`
    let dataCalue = jp.query(data, condition)
    return dataCalue
  }

  getOption() {

    const option = {
      tooltip: {},
      xAxis: {
        type: 'category',
        data: this.getData("languagePair"),
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          data: this.getData("count"),
          type: 'bar',
          smooth: true,
        },
      ],

    }

    return option
  }

  componentDidMount() {

    console.log(data1)

    let chartData = []

    if (chartData && Array.isArray(data1) && data1.length > 10) {
      chartData = data1.slice(0, 10);
    }
    debugger

    if (chartData && chartData.length > 0) {
      let obj = {}
      obj.label = "Others"
      obj.value = 400
      chartData.push(obj)
    }

    this.setState({
      chartData: chartData.length > 0 ? chartData : data1
    })
    console.log(chartData)
  }

  handleOnClick(event) {
    // this.setState({secondRender:true})
    history.push(
      `${process.env.PUBLIC_URL}/parallel-corpus/${event.languagePair}`,
      this.state
    );

  }

  onChartClick = (params) => {
    console.log("sajish", params)
  }

  renderCusomizedLegend = ({ payload }) => {
    debugger
    const style = {
      marginRight: 10,
      color: "#AAA"
    };
    return (
      <div className="customized-legend" style={{ margin: 50 }}>
        {/* {payload.map(entry => {
          const { dataKey, color } = entry;
          const active = _.includes(this.state.disabled, dataKey);
          const style = {
            marginRight: 10,
            color: active ? "#AAA" : "#000"
          }; */}

        {/* return ( */}
        <span
          className="legend-item"
          onClick={() => this.handleMore("dataKey")}
          style={style}
        >
          <Surface width={10} height={10} viewBox="0 0 10 10">
            <Symbols cx={5} cy={5} type="square" size={50} fill={"red"} />
            {/* {active && ( */}
            <Symbols
              cx={5}
              cy={5}
              type="square"
              size={25}
              fill={"#FFF"}
            />
            {/* )} */}
          </Surface>
          <span>more</span>
        </span>
        {/* ); */}
        {/* })} */}
      </div>
    );
  };

  handleMore = () => {
    let chartData =[]
    if (data1 && Array.isArray(data1) && data1.length > 10) {
      console.log(data1.slice(11, 20))
      chartData = data1.slice(11, 20);
    }

    this.setState({
      chartData
    })
  }

  render() {
    const { classes, open_sidebar } = this.props;
    const onEvents = {
      'click': this.onChartClick,
      'legendselectchanged': this.onChartLegendselectchanged
    }
    this.getData()
    return (

      <div>
        <ReactECharts
          option={this.getOption()}
          notMerge={true}
          lazyUpdate={true}
          theme={"theme_name"}
          onEvents={onEvents}
          onChartReady={this.onChartReadyCallback}
          onChartClick={(params) => {
            console.log("sajish")
            // Do what you want to do on click event. params depend on the  type of  chart 
          }}
        />

        <BarChart width={800} height={400} data={data} maxBarSize={100} barSize={80} style={{ marginLeft: '20%', marginTop: "10%" }}>
          <XAxis dataKey="languagePair" />
          <YAxis type="number" />
          <CartesianGrid horizontal={true} vertical={false} />
          <Tooltip />
          <Bar dataKey="count" fill="green" maxBarSize={100} isAnimationActive={false} onClick={(event) => { this.handleOnClick(event) }}>
            {
              data.map((entry, index) => {
                const color = Math.floor(Math.random() * 16777215).toString(16);
                console.log(color)
                return <Cell fill={`#${color}`} />;
              })
            }
          </Bar>
          {/* <Bar dataKey="count" fill={randomColor()} maxBarSize={100} isAnimationActive={false} onClick={(event)=>{this.handleOnClick(event)}}/> */}
        </BarChart>


        {/* {this.state.secondRender && <DrillChartRender />}
            <DrillSourceRender/> */}


        <div style={{padding: "50px"}}>
          <BarChart width={800} height={400} data={this.state.chartData} maxBarSize={100} barSize={80} style={{ marginLeft: '20%', marginTop: "10%" }}>
            <XAxis dataKey="label" />
            <YAxis type="number" />
            <CartesianGrid horizontal={true} vertical={false} />
            <Legend
              verticalAlign="bottom"
              height={36}
              align="left"
              payload={_.toPairs(this.state.chartColors).map(pair => ({
                dataKey: pair[0],
                color: pair[1]
              }))}
              content={this.renderCusomizedLegend}
            />
            <Legend layout="horizontal" verticalAlign="top" align="center" />
            <Tooltip />
            <Bar dataKey="value" fill="green" maxBarSize={100} isAnimationActive={false} onClick={(event) => { this.handleOnClick(event) }}>
              {
                data.map((entry, index) => {
                  const color = Math.floor(Math.random() * 16777215).toString(16);
                  console.log(color)
                  return <Cell fill={`#${color}`} />;
                })
              }
            </Bar>
          </BarChart>
        </div>
      </div>

    )
  }
}

const mapStateToProps = state => ({
  // open_sidebar: state.open_sidebar.open
});

const mapDispatchToProps = dispatch => bindActionCreators(
  {
    APITransport,
    showSidebar
  },
  dispatch
);


export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(withStyles(GlobalStyles(Theme), { withTheme: true })(ChartRender)));
