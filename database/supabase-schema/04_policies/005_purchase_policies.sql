CREATE POLICY "Authorized roles can view purchases entries"
  ON purchases
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );

CREATE POLICY "Admins and operators can insert purchases entries"
  ON purchases
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

CREATE POLICY "Admins and operators can update purchases entries"
  ON purchases
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

CREATE POLICY "Only admins can delete purchases entries"
  ON purchases
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );