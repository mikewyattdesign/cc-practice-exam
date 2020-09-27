export class Question {
    readonly part: string;
    readonly answers: string[];
    readonly index: string;
    readonly prompt: string;
    readonly correct_answer: string;
    readonly rationale: string;
    chosen_answer?: string;

    constructor({
        part,
        answers,
        index,
        prompt,
        correct_answer,
        rationale,
        chosen_answer
    }: {
        part: string;
        answers: string[];
        index: string;
        prompt: string;
        correct_answer: string;
        rationale: string;
        chosen_answer: string | undefined;
    }) {
        this.part = part;
        this.answers = answers;
        this.index = index;
        this.prompt = prompt;
        this.correct_answer = correct_answer;
        this.rationale = rationale;
        this.chosen_answer = chosen_answer;
    }

    get correct(): boolean {
        return this.correct_answer == this.chosen_answer;
    }

    get answered(): boolean {
        return this.chosen_answer !== undefined;
    }
}