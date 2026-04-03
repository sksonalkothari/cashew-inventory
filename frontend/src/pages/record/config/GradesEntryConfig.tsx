import type { FormField } from "../../../types/FormField";
import { GradeTwoTone } from "@mui/icons-material";

export const fields: FormField[] = [
  { name: "grade_name", label: "Name", type: "text", required: true },
];

export const gradesPageMeta = {
  title: "Grades",
  subtitle: "Add new grades",
  icon: <GradeTwoTone fontSize="medium" sx={{ color: "#cc6600" }} />,
};
