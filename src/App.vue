<template>
  <div id="app">
    <div class="question-header">
      <div class="progress">
        <div>{{ answered }} answered out of {{ total }}</div>
        <progress :max="total" :value="answered"></progress>
      </div>

      <div class="prompt">
        <span class="question-index">{{ index }}</span> {{ prompt }}
      </div>
    </div>
    <div class="answers">
      <div
        class="answer"
        :class="{
          submitted:
            letterFromAnswerIndex(answer_index) ==
            currentQuestion.chosen_answer,
          actual:
            complete &&
            letterFromAnswerIndex(answer_index) ==
              currentQuestion.correct_answer,
          wrong:
            complete &&
            letterFromAnswerIndex(answer_index) !=
              currentQuestion.correct_answer &&
            letterFromAnswerIndex(answer_index) ==
              currentQuestion.chosen_answer,
          correct:
            complete &&
            letterFromAnswerIndex(answer_index) ==
              currentQuestion.correct_answer &&
            letterFromAnswerIndex(answer_index) ==
              currentQuestion.chosen_answer,
        }"
        :key="answer_index"
        v-for="(answer, answer_index) in answers"
      >
        <input
          v-model="chosenAnswerIndex"
          type="radio"
          :value="answer_index"
          name="answer"
          :id="`answer_${answer_index}`"
        />
        <label :for="`answer_${answer_index}`">{{ answer }}</label>
      </div>
    </div>
    <div class="rationale" v-if="complete">
      <div class="rationale-title">Rationale</div>
      {{ rationale }}
    </div>
    <div class="navigation">
      <button v-if="!complete && previousEnabled" @click="previousQuestion">
        &larr; Previous
      </button>
      <button v-if="!complete && nextEnabled" @click="nextQuestion">
        Next &rarr;
      </button>
    </div>
    <footer class="question-footer">
      <div class="navigation" v-if="complete">
        <button v-if="previousEnabled" @click="previousQuestion">
          &larr; Previous
        </button>
        <button v-if="nextEnabled" @click="nextQuestion">Next &rarr;</button>
      </div>
      <div class="actions" v-if="!complete">
        <button
          class="primary"
          id="submit"
          :disabled="chosenAnswerIndex == null"
          @click="submitQuestion"
        >
          Submit
        </button>
      </div>
    </footer>
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

  @Getter
  complete !: boolean;

  chosenAnswerIndex: null | number = null;

  public get index() {
    return this.currentQuestionIndex + 1;
  }

  public get prompt(): string {
    return this.currentQuestion.prompt
  }

  public get rationale(): string {
    return this.currentQuestion.rationale;
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
  color: var(--paragraph);
}

:root {
  --padding-x: 16px;
  --background: #fef6e4;
  --headline: #001858;
  --paragraph: #172c66;
  --button: #f582ae;
  --button-text: #001858;
  --stroke: #001858;
  --main: #f3d2c1;
  --highlight: #fef6e4;
  --secondary: #8bd3dd;
  --tertiary: #f582ae;
  --footer-height: 75px;
  --correct: hsl(136deg 73% 70%);
  --wrong: hsl(-4deg 73% 70%);
}

body {
  margin: 0;
  background-color: var(--background);
}

body * {
  box-sizing: border-box;
}

.question-header {
  padding: 1rem var(--padding-x);
}

.progress {
  margin-bottom: 1rem;
}

.answers {
  padding: 1rem 0;
  background-color: var(--main);
}

.answer {
  padding: 1rem var(--padding-x);
}

.answer.submitted {
  background-color: #ddd;
}

.answer.correct,
.answer.actual {
  background-color: var(--correct);
}
.answer.wrong {
  background-color: var(--wrong);
}

.question-index {
  font-size: 2.5em;
  margin-bottom: 0;
  float: left;
  line-height: 1;
  margin: 0 0.5rem 0.25em 0;
}
.question-index::after {
  content: ".";
  margin-right: 0;
}

.prompt {
  line-height: 1.5;
}

.rationale-title {
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.rationale {
  padding: 1rem var(--padding-x);
  line-height: 1.25;
  word-break: break-word;
}

.answer label {
  color: hsl(224deg 63% 25%);
}
.answer input[type="radio"]:checked + label {
  color: hsl(224deg 63% 45%);
}

footer.question-footer {
  position: fixed;
  bottom: 0;
  background-color: #fff;
  width: 100%;
  padding-left: var(--padding-x);
  padding-right: var(--padding-x);
  padding-bottom: 16px;
  padding-top: 8px;
  height: var(--footer-height);
}

.navigation {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--footer-height);
}

.actions {
  display: flex;
  width: 100%;
  justify-content: flex-end;
}

button {
  appearance: none;
  background: none;
  border: none;
  display: block;
  padding: 1rem 1.5rem;
  border: 2px solid transparent;
  border-radius: 0.5rem;
  color: var(--button-text);
}

button:disabled {
  opacity: 0.3;
}

#submit {
  justify-self: flex-end;
}

.primary {
  background-color: var(--button);
}

button:active,
button:focus {
  outline: none;
}

progress {
  width: 100%;
}
</style>
