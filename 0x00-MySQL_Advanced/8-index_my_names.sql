-- creates a stored procedure ComputeAverageScoreForUser that
-- computes and store the average score for a student.

CREATE INDEX idx_name_first
ON names(name(1));
