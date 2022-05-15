import { ActionTypes } from "../constants/action-types";
const intialState = {
  notes: []
};
export const notesReducer = (state = intialState, { type, payload }) => {
  switch (type) {
    case ActionTypes.SET_NOTES:
      return { ...state, notes: payload };
      case ActionTypes.SET_NOTE:
      return { ...state, notes: payload };
    case ActionTypes.REMOVE_SELECTED_NOTE:
      console.log(payload)
      return { ...state, notes: state.notes.filter((note,index) => index !== payload) };

    default:
      return state;
  }
};
export const selectedNotesReducer = (state = {}, { type, payload }) => {
  console.log(type);
  switch (type) {
    case ActionTypes.SELECTED_NOTE:
      return { ...state,payload}
    default:
      return state;
  }
};