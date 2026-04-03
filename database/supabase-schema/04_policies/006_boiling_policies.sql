CREATE POLICY "Authorized roles can view boiling entries"
  ON boiling
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );
CREATE POLICY "Admins and operators can insert boiling entries"
  ON boiling
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );
CREATE POLICY "Admins and operators can update boiling entries"
  ON boiling
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );
CREATE POLICY "Only admins can delete boiling entries"
  ON boiling
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );