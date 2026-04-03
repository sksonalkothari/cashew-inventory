-- SELECT: Admins, Operators, Viewers
CREATE POLICY "Authorized roles can view cashew kernel sales"
  ON cashew_kernel_sales
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );

-- INSERT: Admins and Operators
CREATE POLICY "Admins and operators can insert cashew kernel sales"
  ON cashew_kernel_sales
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

-- UPDATE: Admins and Operators
CREATE POLICY "Admins and operators can update cashew kernel sales"
  ON cashew_kernel_sales
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2)
    )
  );

-- DELETE: Admins Only
CREATE POLICY "Only admins can delete cashew kernel sales"
  ON cashew_kernel_sales
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id = 1
    )
  );