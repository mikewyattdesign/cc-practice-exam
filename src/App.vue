<template>
  <div id="app">
    <div class="question-header">
      <div class="progress">
        <div>{{ answered }} answered out of {{ total }}</div>
        <progress :max="total" :value="answered"></progress>
      </div>
      <div class="question-index">{{ index }}</div>
      <div class="prompt">{{ prompt }}</div>
    </div>
    <div class="answers">
      <div class="answer" :class="{'submitted': letterFromAnswerIndex(answer_index) == currentQuestion.chosen_answer}" :key="answer_index" v-for="(answer, answer_index) in answers">
        <input v-model="chosenAnswerIndex" type="radio" :value="answer_index" name="answer" :id="`answer_${answer_index}`">
        <label :for="`answer_${answer_index}`">{{ answer }}</label>
      </div>
    </div>
    <div class="actions">
      <button v-if="previousEnabled" @click="previousQuestion">&larr; Previous</button>
      <button :disabled="chosenAnswerIndex == null" @click="submitQuestion">Submit</button>
      <button v-if="nextEnabled" @click="nextQuestion">Next &rarr;</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { State, Getter, Mutation } from 'vuex-class';
import { Question } from './models/question' // eslint-disable-line

@Component({
  components: {
  },
})
export default class App extends Vue {
  @State
  currentQuestionIndex !: number;

  @Watch('currentQuestionIndex')
  handleQuestionUpdate() {
    if (this.currentQuestion.chosen_answer == undefined) {
      this.chosenAnswerIndex = null
      return
    }

    if (typeof this.currentQuestion.chosen_answer == 'string') {
      this.chosenAnswerIndex = this.currentQuestion.chosen_answer.charCodeAt(0) - 65
    }
  }

  @Getter
  currentQuestion !: Question;

  @Getter
  nextEnabled !: boolean;

  @Getter
  previousEnabled !: boolean;

  @Getter
  answered !: number;

  @Getter
  total !: number

  chosenAnswerIndex: null | number = null;

  public get index() {
    return this.currentQuestionIndex + 1;
  }

  public get prompt(): string {
    return this.currentQuestion.prompt
  }

  public get answers(): string[] {
    return this.currentQuestion.answers
  }

  public get selectedAnswer(): string | undefined {
    if (this.chosenAnswerIndex == null) return undefined
    return this.letterFromAnswerIndex(this.chosenAnswerIndex)
  }

  public letterFromAnswerIndex(index: number): string {
    return String.fromCharCode(65 + index)
  }

  @Mutation 
  previousQuestion !: () => void;
  
  @Mutation 
  nextQuestion !: () => void;

  

  @Mutation 
  saveQuestion !: (payload: string | undefined) => void;

  submitQuestion() {
    this.saveQuestion(this.selectedAnswer)
  }
}
</script>

<style>
#app {
  font-family: sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

:root {
  --padding-x: 16px;
}

body{
  margin: 0;
}

.question-header {
  padding: 1rem var(--padding-x);
}

.progress {
  margin-bottom: 1rem;  
}

.answers {
  padding: 1rem 0;
  background-color: #eee;
}

.answer {
  padding: 1rem var(--padding-x);
}

.answer.submitted {
  background-color: #ddd;
}

.answer.correct {
  border-color: #2d5;
}

.question-index {
  font-size: 2.5em;
  margin-bottom: 1rem;
}
.question-index::after {
  content: '.';
  margin-right: 0.5em;
}

.prompt {
  line-height: 1.5;
}

.answer label {
  color: #999;
}
.answer input[type="radio"]:checked + label {
  color: #333;
}

.actions {
  display: flex;
  padding: 1rem var(--padding-x);
  justify-content: space-evenly;
}

button {
  appearance: none;
  background: none;
  border: none;
}

button:active,
button:focus {
  outline: none;
}

progress {
  width: 100%;
}
</style>
