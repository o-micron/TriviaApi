import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      categories: [],
      difficulties: []
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: result => {
        console.log(result.categories);
        this.setState({
          categories: result.categories
        });
        return;
      },
      error: error => {
        alert("Unable to load categories. Please try your request again");
        return;
      }
    });

    $.ajax({
      url: `/difficulties`, //TODO: update request URL
      type: "GET",
      success: result => {
        this.setState({
          difficulties: result.difficulties
        });
        return;
      },
      error: error => {
        alert("Unable to load difficulties. Please try your request again");
        return;
      }
    });
  }

  submitQuestion = event => {
    let data = JSON.stringify({
      question: this.refs.question.value,
      answer: this.refs.answer.value,
      difficultyId: parseInt(this.refs.difficulty.value),
      categoryId: parseInt(this.refs.category.value)
    });
    console.log(data);
    event.preventDefault();
    $.ajax({
      url: "/questions", //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: data,
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: result => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: error => {
        console.log(error);
        alert("Unable to add question. Please try your request again");
        return;
      }
    });
  };

  render() {
    return (
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form
          className="form-view"
          id="add-question-form"
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input ref="question" type="text" name="question" />
          </label>
          <label>
            Answer
            <input ref="answer" type="text" name="answer" />
          </label>
          <label>
            Difficulty
            <select ref="difficulty" name="difficulty">
              {Object.keys(this.state.difficulties).map(id => {
                return (
                  <option
                    key={this.state.difficulties[id].id}
                    value={this.state.difficulties[id].id}
                  >
                    {this.state.difficulties[id].level}
                  </option>
                );
              })}
            </select>
          </label>
          <label>
            Category
            <select ref="category" name="category">
              {Object.keys(this.state.categories).map(id => {
                return (
                  <option
                    key={this.state.categories[id].id}
                    value={this.state.categories[id].id}
                  >
                    {this.state.categories[id].name}
                  </option>
                );
              })}
            </select>
          </label>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
