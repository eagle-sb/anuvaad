import React from "react";
import { withRouter } from "react-router-dom";
import { bindActionCreators } from "redux";
import { connect } from "react-redux";
import Toolbar from "@material-ui/core/Toolbar";
import AppBar from "@material-ui/core/AppBar";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";
import Pagination from "@material-ui/lab/Pagination";
import TextField from '@material-ui/core/TextField'
import SENTENCE_ACTION from "./SentenceActions";
import Slider from '@material-ui/core/Slider';
import Tooltip from '@material-ui/core/Tooltip';
import PropTypes from 'prop-types';
import { currentPageUpdate } from "../../../../flux/actions/apis/document_translate/pagiantion_update";
import { clearHighlighBlock } from '../../../../flux/actions/users/translator_actions';
import fetchpercent from '../../../../flux/actions/apis/view_digitized_document/fetch_slider_percent';
import fetchfontpixel from '../../../../flux/actions/apis/view_digitized_document/fetch_slider_pixel';

const PAGE_OPS = require("../../../../utils/page.operations");


function ValueLabelComponent(props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
      {children}
    </Tooltip>
  );
}

ValueLabelComponent.propTypes = {
  children: PropTypes.element.isRequired,
  open: PropTypes.bool.isRequired,
  value: PropTypes.number.isRequired,
};

class InteractivePagination extends React.Component {
  constructor(props) {
    super(props);
    this.state = { offset: 1, gotoValue: 1 };
  }
  handleClick = (offset, value) => {
    this.props.currentPageUpdate(value);
    this.setState({ offset: value, gotoValue: value });
  };

  componentDidMount() {
    this.props.currentPageUpdate(1);
  }

  sentenceCount = () => {
    let sentenceCount = PAGE_OPS.get_sentence_count(
      this.props.data,
      this.state.offset
    );
    return sentenceCount;
  };

  sentenceProgress = () => {
    let sentenceProgressCount = PAGE_OPS.get_total_sentence_count(
      this.props.job_details,
      this.props.match.params.inputfileid
    );
    return sentenceProgressCount;
  };

  /**
   * Merge mode user action handlers
   */
  processMergeButtonClicked = () => {
    this.props.clearHighlighBlock();
    this.props.onAction(SENTENCE_ACTION.START_MODE_MERGE, this.state.offset);
  };

  processMergeNowButtonClicked = () => {
    if (this.props.onAction) {
      this.props.onAction(SENTENCE_ACTION.SENTENCE_MERGED, this.state.offset);
    }
  };

  handlePageClick = () => {
    this.handleClick("", parseInt(this.state.gotoValue))
    this.setState({ offset: parseInt(this.state.gotoValue) })
  }

  renderNormaModeButtons = () => {
    return (
      <div>
        <Button
          onClick={this.processMergeButtonClicked}
          variant="outlined"
          color="primary"
        >
          MERGE
        </Button>
      </div>
    );
  };


  renderMergeModeButtons = () => {
    return (
      <div>
        <Button
          style={{ marginRight: "10px" }}
          onClick={this.processMergeNowButtonClicked}
          variant="outlined"
          color="primary"
        >
          MERGE NOW
        </Button>
        <Button
          onClick={this.processMergeCancelButtonClicked}
          variant="outlined"
          color="primary"
        >
          CANCEL MERGE
        </Button>
      </div>
    );
  };

  processMergeCancelButtonClicked = () => {
    this.props.onAction(SENTENCE_ACTION.END_MODE_MERGE, this.state.offset);
  };

  handleTextValueChange = (event) => {
    this.setState({ gotoValue: event.target.value })
  }

  setConfPercentage = (event) => {
    console.log(event.target.value)
  }

  adjustFontPixel = (event, pixel) => {
    this.props.fetchfontpixel(pixel)
  }

  footer = () => {
    return (
      <AppBar
        position={"fixed"}
        style={{
          top: 'auto',
          bottom: 0,
          // marginTop: "13px"
        }}
        color="secondary"
      >
        <Toolbar
          disableGutters={!this.props.open_sidebar}
          style={{ height: "65px" }}
        >
          {this.props.document_editor_mode.mode === "EDITOR_MODE_MERGE" ? (
            <div style={{ position: "absolute", right: "30px" }}>
              {this.renderMergeModeButtons()}
            </div>
          ) : (
            <>
              {this.props.processZoom()}
              <Pagination
                count={this.props.count}
                page={this.state.offset}
                onChange={this.handleClick}
                color="primary"
                size={"large"}
                style={{ marginLeft: "-8.5%" }}
              />
              <TextField
                type="number"
                style={{ width: "40px" }}
                InputProps={{

                  inputProps: {
                    style: { textAlign: "center" },
                    max: this.props.count, min: 1
                  }
                }}
                onChange={(event) => { this.handleTextValueChange(event) }}
                value={this.state.gotoValue}
              />
              <Button
                onClick={this.handlePageClick}
                style={{ marginLeft: '6px' }}
                variant="outlined"
                color="primary"
                disabled={this.state.offset === Number(this.state.gotoValue) && true}
              >
                GO
        </Button>
              {(!this.props.show_pdf && !this.props.hideMergeBtn) &&
                <>
                  {this.sentenceCount() && (
                    <div style={{ position: "absolute", marginLeft: "62%" }}>
                      <Typography variant="subtitle1" component="h2">
                        Page Sentences
                        </Typography>

                      <div style={{ textAlign: "center" }}>
                        {this.sentenceCount()}
                      </div>
                    </div>
                  )}

                  {this.props.job_status && this.props.job_status.word_status && <div style={{ position: "absolute", marginLeft: "70%" }}>
                    <Typography variant="subtitle1" component="h2">
                      Total Word Count
                      </Typography>

                    <div style={{ textAlign: "center" }}>
                      {this.props.job_status.word_status && this.props.job_status.word_status}
                    </div>
                  </div>}

                  {this.props.job_status && this.props.job_status.status &&
                    <div style={{ position: "absolute", marginLeft: "79%" }}>
                      <Typography variant="subtitle1" component="h2">
                        Total Sentences
                      </Typography>

                      <div style={{ textAlign: "center" }}>
                        {this.props.job_status.status && this.props.job_status.status}
                      </div>
                    </div>}

                  <div style={{ position: "absolute", right: "30px" }}>
                    {this.renderNormaModeButtons()}
                  </div>
                </>
              }
              {/* {
                  this.props.showConfSlider &&
                  <div style={{ display: 'grid', marginTop: '1%', width: '20%', gridTemplateColumns: 'repeat(1,40% 80%)' }}>
                    <Typography style={{ marginLeft: '15%', color: 'black' }} id="discrete-slider-always" gutterBottom>
                      Confidence Score
                    </Typography>
                    <Slider
                      ValueLabelComponent={ValueLabelComponent}
                      aria-label="custom thumb label"
                      defaultValue={80}
                      onChange={this.handleSliderChange}
                    />
                  </div>
                } */}
              {
                this.props.showFontAdjuster &&
                <div style={{ display: 'grid', marginTop: '1%', width: '20%', gridTemplateColumns: 'repeat(1,40% 80%)' }}>
                  <Typography style={{ marginLeft: '15%', color: 'black' }} id="discrete-slider-always" gutterBottom>
                    Adjust Font
                    </Typography>
                  <Slider
                    ValueLabelComponent={ValueLabelComponent}
                    aria-label="custom thumb label"
                    defaultValue={this.props.fontSize}
                    onChange={this.adjustFontPixel}
                  />
                </div>
              }

            </>
          )}
        </Toolbar>
      </AppBar>
    )
  }

  render() {

    return (
      this.footer()
    );
  }
}

const mapStateToProps = (state) => ({
  document_editor_mode: state.document_editor_mode,
  job_details: state.job_details,
  show_pdf: state.show_pdf.open,
  job_status: state.job_status,
  fontSize: state.fetch_slider_pixel.percent
});

const mapDispatchToProps = (dispatch) =>
  bindActionCreators(
    {
      currentPageUpdate,
      clearHighlighBlock,
      fetchpercent,
      fetchfontpixel,
    },
    dispatch
  );

export default withRouter(
  connect(mapStateToProps, mapDispatchToProps)(InteractivePagination)
);
