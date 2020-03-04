import React, { Component } from "react";

import "../stylesheets/App.css";
import Question from "./Question";
import Search from "./Search";
import $ from "jquery";

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      questionsPerPage: 0,
      categories: [],
      currentCategory: null
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    this.setState({ currentCategory: null });
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions,
          questionsPerPage: result.questionsPerPage,
          categories: result.categories
        });
        return;
      },
      error: error => {
        alert("Unable to load questions. Please try your request again");
        return;
      }
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(
      this.state.totalQuestions / this.state.questionsPerPage
    );
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? "active" : ""}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = category => {
    this.setState({ currentCategory: category }, () => {
      $.ajax({
        url: `/categories/${this.state.currentCategory.id}/questions`, //TODO: update request URL
        type: "GET",
        success: result => {
          this.setState({
            questions: result.questions,
            totalQuestions: result.totalQuestions
          });
          return;
        },
        error: error => {
          alert("Unable to load questions. Please try your request again");
          return;
        }
      });
    });
  };

  submitSearch = (query, category) => {
    $.ajax({
      url: `/questions/search`, //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        query: query,
        categoryId: category != null ? category.id : -1
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.totalQuestions
        });
        return;
      },
      error: error => {
        alert("Unable to load questions. Please try your request again");
        return;
      }
    });
  };

  questionAction = id => action => {
    if (action === "DELETE") {
      if (window.confirm("are you sure you want to delete the question?")) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: result => {
            this.getQuestions();
          },
          error: error => {
            alert("Unable to load questions. Please try your request again");
            return;
          }
        });
      }
    }
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {this.state.categories.map((c, ind) => (
              <li
                key={c.id}
                onClick={() => {
                  this.getByCategory(c);
                }}
              >
                {c.name}
                <img className="category" src={`${c.name}.svg`} alt="" />
              </li>
            ))}
          </ul>
          <Search
            submitSearch={this.submitSearch}
            category={this.state.currentCategory}
          />
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.category}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
