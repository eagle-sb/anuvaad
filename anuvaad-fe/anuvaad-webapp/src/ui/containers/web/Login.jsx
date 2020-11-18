import React from "react";
import { MuiThemeProvider } from "@material-ui/core/styles";
import { withRouter } from "react-router-dom";
import PropTypes from "prop-types";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";
import Checkbox from "@material-ui/core/Checkbox";
import InputLabel from "@material-ui/core/InputLabel";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Input from "@material-ui/core/Input";
import FormControl from "@material-ui/core/FormControl";
// import {Link} from 'react-router';
import { connect } from "react-redux";
import { bindActionCreators } from "redux";
import { withStyles } from "@material-ui/core";
import ThemeDefault from "../../theme/web/theme-anuvaad";
import LoginStyles from "../../styles/web/LoginStyles";
import LoginAPI from "../../../flux/actions/apis/login";
import APITransport from "../../../flux/actions/apitransport/apitransport";
import history from "../../../web.history";
import { translate } from "../../../assets/localisation";
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';

const TELEMETRY = require('../../../utils/TelemetryManager')

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      password: ""
    };
  }

  getSnapshotBeforeUpdate(prevProps, prevState) {
    TELEMETRY.pageLoadStarted('login')
    /**
    * getSnapshotBeforeUpdate() must return null
    */
    return null;
  }
  componentDidUpdate(prevProps, prevState, snapshot) {
  }

  componentDidMount() {
    localStorage.removeItem("token");
    TELEMETRY.pageLoadCompleted('login')
  }

  /**
   * user input handlers
   * captures text provided in email and password fields
   */

  processInputReceived = prop => event => {
    this.setState({ [prop]: event.target.value });
  };

  /**
   * user input handlers
   * captures form submit request
   */
  processLoginButtonPressed = () => {
    const { email, password } = this.state;
    const { APITransporter } = this.props;

    // const apiObj = new LoginAPI(email, password);

    const apiObj = new LoginAPI("vishal@123", "Vishal@123");

    // if ((email == "aroop" || email == "ajitesh" || email == "kd" || email == "vivek") && password == "test") {
    //   localStorage.setItem("token", "123");
    //   setTimeout(() => {
    //     history.push(`${process.env.PUBLIC_URL}/corpus`);
    //   }, 1000);
    // } else {
    //   alert(translate('login.page.alert.wrongCredentials'));
    // }
    // APITransporter(apiObj);

    const apiReq = fetch(apiObj.apiEndPoint(), {
      method: 'post',
      body: JSON.stringify(apiObj.getBody()),
      headers: apiObj.getHeaders().headers
    }).then(async response => {
      const rsp_data = await response.json();
      if (!response.ok) {
        return Promise.reject('');
      } else {
        console.log(rsp_data)
        let resData = rsp_data && rsp_data.data
        localStorage.setItem("token", resData.token)

        history.push(`${process.env.PUBLIC_URL}/view-document`);

      }
    }).catch((error) => {
      console.log('api failed because of server or network')
    });
  };

  render() {
    return (
      <MuiThemeProvider theme={ThemeDefault}>
      <div style={{ width: "100%", height: window.innerHeight, display: "flex", flexDirection: "column", textAlign: "center" }}>
        <div style={{ marginTop: "5%" }}>
          <Typography style={{ fontWeight: '550', fontSize: "36px", color: "#233466" }}>
            Sign In
        </Typography>
          <Paper style={{ width: "40%", marginLeft: '30%', marginTop: "3%", textAlign: "center", alignItems: "center", display: "flex", flexDirection: "column" }}>
            <FormControl fullWidth style={{ alignItems: "center", display: "flex", flexDirection: "column" }}>

              <TextField
                label="Email/UserName"
                type="text"
                name="email"
                fullWidth
                value={this.state.email}
                onChange={this.processInputReceived('email')}
                variant="outlined"
                style={{ width: '50%', border: "grey", marginTop: "60px" }}

              />


              <TextField
                label="Password"
                type="password"
                name="password"
                fullWidth
                value={this.state.password}
                onChange={this.processInputReceived('password')}
                variant="outlined"
                style={{ width: '50%', border: "grey", marginTop: "40px" }}

              />

              <Button
                disabled={!this.state.termsAndCondition}
                variant="contained" aria-label="edit" style={{
                  width: '50%', marginBottom: '60px', marginTop: '40px', borderRadius: '20px', height: '45px', textTransform: 'initial', fontWeight: '20px',
                  color: "#FFFFFF",
                  backgroundColor: "#1C9AB7",
                }} onClick={this.processLoginButtonPressed.bind(this)}>
                {translate('singUp.page.label.signUp')}
              </Button>
            </FormControl>
          </Paper>
        </div>
      </div>
       </MuiThemeProvider>
    )
  }
}

Login.propTypes = {
  user: PropTypes.object.isRequired,
  APITransporter: PropTypes.func.isRequired
};

const mapStateToProps = state => ({
  user: state.login
});

const mapDispatchToProps = dispatch =>
  bindActionCreators(
    {
      APITransporter: APITransport
    },
    dispatch
  );

export default withRouter(
  withStyles(LoginStyles)(
    connect(
      mapStateToProps,
      mapDispatchToProps
    )(Login)
  )
);
