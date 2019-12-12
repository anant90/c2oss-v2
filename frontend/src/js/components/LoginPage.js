import React from 'react';
import {Link} from 'react-router';

class LoginPage extends React.Component{
  render(){
    return (
      <div className="landing-page-wrapper">
        <div className="landing-page">
          <Link className="home-link" to="/">contributetooss.org</Link>
          <h1 className="landing-logo">Contribute to Open Source Software</h1>
          <div className="landing-copy">
            <p>This little tool helps you to contribute more to open source projects you like by helping you find open issues to work on.</p>
            <p>It aggregates open issues marked as bugs or enhancements in the public Github repositories you have starred or are a member of.</p>
          </div>
          <a href="/login/github/">
            <div className="login-button">
              <span className="github-logo" />
              <span className="cta">Get started with Github</span>
            </div>
          </a>
          <div className="reassurance-wrapper">
            <div className="reassurance">We ask access only to your public data</div>
          </div>
        </div>
      </div>
    )
  }
};

export default LoginPage;
