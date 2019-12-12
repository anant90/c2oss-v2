import React from 'react';
import {Link} from 'react-router';

class HeroUnit extends React.Component{
  render(){
    return (
      <div className="hero-unit">
        <div className="user-box">
          <Link className="home-link" to="/">c2oss.com</Link>
          <div className="user-info">
            <img className="avatar-image" src={this.props.avatar_url}/>
            <div className="shifted-right">
              <span className="name">{this.props.name}</span>
              <span className="username">{this.props.login}</span>
            </div>
          </div>
        </div>
        <div className="user-stats">
          <table>
            <tbody>
              <tr><td>{this.props.starred_repos_count}</td><td>Starred Public Repositories</td></tr>
              <tr><td>{this.props.total_issues_count}</td><td>Issues</td></tr>
              <tr className="blank-row" />
              <tr><td>{this.props.bugs_count}</td><td>Bugs</td></tr>
              <tr><td>{this.props.enhancements_count}</td><td>Enhancements</td></tr>
              <tr><td>{this.props.unassigned_issues_count}</td><td>Unassigned</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    )
  }
};

export default HeroUnit;
