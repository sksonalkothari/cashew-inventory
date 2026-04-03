-- SELECT: Admins, Operators, Viewers
CREATE POLICY "Authorized roles can view husk/rejection sales"
  ON husk_rejection_sales
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );

-- INSERT: Admins and Operators
CREATE POLICY "Admins and operators can insert husk/rejection sales"
  ON husk_rejection_sales
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

-- UPDATE: Admins and Operators
CREATE POLICY "Admins and operators can update husk/rejection sales"
  ON husk_rejection_sales
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

-- DELETE: Admins Only
CREATE POLICY "Only admins can delete husk/rejection sales"
  ON husk_rejection_sales
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );