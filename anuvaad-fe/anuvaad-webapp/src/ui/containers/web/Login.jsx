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
       localStorage.setItem("token", "6d39df2f57f0418a9bfd0ba6dc48cd2b%7Cad7694537c48416cb579519f3419709e")
       localStorage.setItem("roles", ["editor", "dev", "interactive-editor", "grader"])
       debugger
       history.push(`${process.env.PUBLIC_URL}/view-document`);

      }
    }).catch((error) => {
      console.log('api failed because of server or network')
    });
  };

  //   render() {
  //     const { user, classes, location } = this.props;
  //     return (
  //       <MuiThemeProvider theme={ThemeDefault}>
  //         <div>
  //           <div className={classes.loginContainer}>
  //             <Paper className={classes.paper}>
  //               <form method="post">
  //                 <FormControl fullWidth>
  //                   <InputLabel htmlFor="email">{translate('common.page.label.name')}</InputLabel>
  //                   <Input id="email" floatingLabelText="E-mail" onChange={this.processInputReceived("email")} />
  //                 </FormControl>
  //                 <FormControl fullWidth>
  //                   <InputLabel htmlFor="password">{translate('common.page.label.password')}</InputLabel>
  //                   <Input id="password" floatingLabelText="Password" type="password" onChange={this.processInputReceived("password")} />
  //                 </FormControl>
  //                 <div>
  //                   <FormControlLabel
  //                     control={
  //                       <Checkbox
  //                         className={classes.checkRemember.className}
  //                         labelclassName={classes.checkRemember.labelclassName}
  //                         iconclassName={classes.checkRemember.iconclassName}
  //                       />
  //                     }
  //                     label={translate('login.page.label.remeberMe')}
  //                   />

  //                   {/* <Link to="/"> */}
  //                   <Button variant="contained" onClick={this.processLoginButtonPressed} color="secondary" aria-label="edit">
  //                     {translate('common.page.button.login')}
  //                   </Button>
  //                   {/* </Link> */}
  //                 </div>
  //               </form>
  //             </Paper>

  //             <div className={classes.buttonsDiv} />
  //           </div>
  //         </div>
  //       </MuiThemeProvider>
  //     );
  //   }
  // }

  render() {
    const { user, classes, location } = this.props;
    return (
      <div style={{ width: "100%", height: window.innerHeight, display: "flex", flexDirection: "column", textAlign: "center" }}>
        <div style={{ display: 'flex', flexDirection: 'column', flex: 1, alignItems: 'center', paddingTop: "5%" }}>
          <Typography variant="h4" style={{ fontWeight: '450', color: '#000000' }}>Sign In</Typography>
          <Paper className={classes.paper}>
            <form method="post">
              <FormControl fullWidth>
                <InputLabel htmlFor="email">{translate('common.page.label.name')}</InputLabel>
                <Input id="email" floatingLabelText="E-mail" onChange={this.processInputReceived("email")} />
              </FormControl>
              <FormControl fullWidth>
                <InputLabel htmlFor="password">{translate('common.page.label.password')}</InputLabel>
                <Input id="password" floatingLabelText="Password" type="password" onChange={this.processInputReceived("password")} />
              </FormControl>
              <div>
                <FormControlLabel
                  control={
                    <Checkbox
                      className={classes.checkRemember.className}
                      labelclassName={classes.checkRemember.labelclassName}
                      iconclassName={classes.checkRemember.iconclassName}
                    />
                  }
                  label={translate('login.page.label.remeberMe')}
                />

                {/* <Link to="/"> */}
                <Button variant="contained" onClick={this.processLoginButtonPressed} color="secondary" aria-label="edit">
                  {translate('common.page.button.login')}
                </Button>
                {/* </Link> */}
              </div>
            </form>
          </Paper>
        </div>
      </div>
    );
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
