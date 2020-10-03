import Vue from 'vue'
import Vuex from 'vuex'
import originalQuestionSet from "../../questions.json"
import { Question } from '../models/question'
Vue.use(Vuex)



function shuffle(array: any[]) {
  let i = array.length - 1;
  for (i; i > 0; i--) {
    const j = Math.floor(Math.random() * i)
    const temp = array[i]
    array[i] = array[j]
    array[j] = temp
  }
  return array;
}

export function getAnsweredQuestions(): any[] {
  let answeredQuestions = [];
  if (localStorage.getItem('questions') != null) {
    answeredQuestions = JSON.parse(localStorage.getItem('questions') as string);
  }

  return answeredQuestions;
}

export function saveAnsweredQuestions(newQuestions: Question[]) {
  let answeredQuestions = getAnsweredQuestions();
  answeredQuestions = answeredQuestions.concat(...newQuestions.map(value => ({
    part: value.part,
    index: value.index,
    correct_answer: value.correct_answer,
    chosen_answer: value.chosen_answer,
    answers: value.answers,
    prompt: value.prompt,
    rationale: value.rationale,
  })));

  localStorage.setItem('questions', JSON.stringify(answeredQuestions));
}

export default new Vuex.Store({
  state: {
    currentQuestionIndex: 0,
    questions: shuffle(
      originalQuestionSet
        .filter((original: any) => (getAnsweredQuestions() as any[]).indexOf((target: any) => target.part == original.part && target.index == original.index) < 0)
    )
      .slice(0, 25).map((value) => new Question(value))
  },
  mutations: {
    previousQuestion(state) {
      state.currentQuestionIndex--;
    },
    nextQuestion(state) {
      state.currentQuestionIndex++;
    },
    saveQuestion(state, payload: string) {
      (state.questions[state.currentQuestionIndex] as Question).chosen_answer = payload;
    },
    saveQuestions(state) {
      saveAnsweredQuestions(state.questions);
    }
  },
  actions: {
  },
  getters: {
    currentQuestion(state): Question {
      return state.questions[state.currentQuestionIndex]
    },
    previousEnabled(state): boolean {
      return state.currentQuestionIndex > 0;
    },
    nextEnabled(state): boolean {
      return state.currentQuestionIndex < state.questions.length - 1;
    },
    answered(state): number {
      return state.questions.filter((question) => question.answered).length
    },
    total(state): number {
      return state.questions.length;
    },
    complete(_, getters): boolean {
      return getters.answered == getters.total;
    }
  }
})
