import React from 'react';
import TimeAgo from 'react-timeago';

class Assignee extends React.Component{
  render() {
    return (
      <div className="assignee">
        . Assigned to <a href={this.props.url} target="_blank">{this.props.login}</a>.
      </div>
    )
  }
};

class Issue extends React.Component{
  render(){
    return (
      <div className="issue">
        <div className="float-left">
          <div className="index">{this.props.index}.</div>
          <a target="_blank" href={this.props.html_url}>
            <div className="title">{this.props.title}</div>
          </a>
          <div className="byline">
            #{this.props.number} opened <TimeAgo date={this.props.github_created_at} /> by <a href={this.props.owner.html_url} target="_blank">{this.props.owner.login}</a>
            {this.props.assignee.login? <Assignee url={this.props.assignee.html_url} login={this.props.assignee.login} /> : ""}
          </div>
        </div>
        <div className="float-right">
          <a target="_blank" href={this.props.html_url}>
            <div className="repo">{this.props.repo_full_name}</div>
            <div className="comments-count">{this.props.comments_count} comments</div>
          </a>
        </div>
      </div>
    )
  }
};

export default Issue;
