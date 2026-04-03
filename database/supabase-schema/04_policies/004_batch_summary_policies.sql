CREATE POLICY "Authorized roles can view batch summary entries"
  ON batch_summary
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );

CREATE POLICY "Admins and operators can insert batch summary entries"
  ON batch_summary
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

CREATE POLICY "Admins and operators can update batch summary entries"
  ON batch_summary
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

CREATE POLICY "Only admins can delete batch summary entries"
  ON batch_summary
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );