import React, { useState } from "react";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import MoreVertIcon from '@mui/icons-material/MoreVert';
const options = [
  'ON',
  'OFF',
];
export const RelayControl = (props) => {
  const ip = props.ip
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
      setAnchorEl(null);
    };
  	const handleSubmit = async (e) => {
      e.preventDefault();
      if (e.currentTarget.textContent === "ON") {
        var relayState = "low"
      } else {
        relayState = "high"
      }
      const payload={
        ip:ip,
        state:relayState
      }
      const response = await axios
      .get("/relay_control",payload)
      .catch((err) => {
        console.log("Err: ", err);
      });
      if (response.status === 200) {
        console.log(response.data)
        setAnchorEl(null);
      }
    };
  return (
    <div>
      <IconButton
          aria-label="more"
          id="long-button"
          aria-controls={open ? 'long-menu' : undefined}
          aria-expanded={open ? 'true' : undefined}
          aria-haspopup="true"
          onClick={handleClick}
        >
          <MoreVertIcon />
        </IconButton>
        <Menu
          id="long-menu"
          MenuListProps={{
            'aria-labelledby': 'long-button',
          }}
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
        >
          {options.map((option) => (
            <MenuItem key={option} selected={option === 'ON'} onClick={handleSubmit}>
              {option}
            </MenuItem>
          ))}
        </Menu>
      </div>
  )
}
