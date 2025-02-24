import * as React from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Chip from "@mui/material/Chip";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 2;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 50,
    },
  },
  anchorOrigin: {
    vertical: "top",
    horizontal: "left",
  },
  transformOrigin: {
    vertical: "bottom",
    horizontal: "left",
  },
};

const semesters = [
  "Spring 2021",
  "Fall 2021",
  "Spring 2022",
  "Fall 2022",
  "Spring 2023",
  "Fall 2023",
  "Spring 2024",
  "Fall 2024",
  "Spring 2025",
  "All semesters",
].reverse();

function getStyles(name, selectedSemesters, theme) {
  return {
    fontWeight: selectedSemesters.includes(name)
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

export default function MultipleSelectChip({
  selectedSemesters,
  setSelectedSemesters,
}) {
  const theme = useTheme();

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;

    if (value.length !== 0) {
      setSelectedSemesters(
        typeof value === "string" ? value.split(",") : value,
      );
    }
  };

  return (
    <div>
      <FormControl
        sx={{
          borderRadius: "14px",
          border: "1px #5E5E5E solid",
          margin: "8px 8px 0",
          width: "auto",
          minWidth: 300,
        }}
      >
        <Select
          variant="outlined"
          sx={{
            "& .MuiChip-root": {
              height: "auto",
              borderRadius: "9.5px",
            },
            "& .MuiOutlinedInput-input": { p: "8px 5px" },
            "& .MuiOutlinedInput-notchedOutline": {
              border: "none",
            },
            "& .MuiSelect-icon": { color: "#454545" },
          }}
          labelId="demo-multiple-chip-label"
          id="demo-multiple-chip"
          multiple
          value={selectedSemesters}
          onChange={handleChange}
          input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => (
                <Chip
                  sx={{ backgroundColor: "grey" }}
                  key={value}
                  label={value}
                />
              ))}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {semesters.map((name) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, selectedSemesters, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
}
