CREATE POLICY "Authorized roles can view peeling before drying entries"
  ON peeling_before_drying
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );
CREATE POLICY "Admins and operators can insert peeling before drying entries"
  ON peeling_before_drying
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );
CREATE POLICY "Admins and operators can update peeling before drying entries"
  ON peeling_before_drying
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );
CREATE POLICY "Only admins can delete peeling before drying entries"
  ON peeling_before_drying
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );