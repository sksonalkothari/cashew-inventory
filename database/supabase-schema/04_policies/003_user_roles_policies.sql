-- Admins can manage user_roles
-- These policies are giving error 
--{
--    "code": "42P17",
--    "details": null,
--    "hint": null,
--    "message": "infinite recursion detected in policy for relation \"user_roles\""
--}
--Hence dropping these policies
CREATE POLICY "Authorized roles can view user roles entries"
  ON user_roles
  FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM user_roles AS ur
      WHERE ur.user_id = (SELECT auth.uid())
    )
  );

CREATE POLICY "Authorized roles can view user roles entries"
  ON user_roles
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = (SELECT auth.uid())
      AND user_roles.role_id IN (1, 2, 3)
    )
  );