import React from 'react';
import {Link} from 'react-router';
import LoginPage from './LoginPage';
import Dashboard from './Dashboard';

class Home extends React.Component{
  render(){
    return (
      <div>
        {window.isLoggedIn ? <Dashboard /> : <LoginPage />}
      </div>
    )
  }
};

export default Home;
