import { ActionTypes } from "../constants/action-types";

export const setNotes = (notes) => {
  return {
    type: ActionTypes.SET_NOTES,
    payload: notes,
  };
};

export const selectedNote = (note) => {
  return {
    type: ActionTypes.SELECTED_NOTE,
    payload: note,
  };
};
export const setNote = (note) => {
  return {
    type: ActionTypes.SET_NOTE,
    payload: note,
  };
};
export const removeNote = (index) => {
  return {
    type: ActionTypes.REMOVE_SELECTED_NOTE,
    payload: index,
  };
};