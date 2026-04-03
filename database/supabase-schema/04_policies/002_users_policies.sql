-- Active users can view their own profile
CREATE POLICY "Users can view their own profile"
  ON users
  FOR SELECT
  USING (
    (SELECT auth.uid()) = id AND status = 'active'
  );

-- Active users can update their own profile
CREATE POLICY "Users can update their own profile"
  ON users
  FOR UPDATE
  USING (
    (SELECT auth.uid()) = id AND status = 'active'
  );

-- users can insert their own profile
CREATE POLICY "Users can insert their own profile"
  ON users
  FOR INSERT
  WITH CHECK (
    auth.uid() = id
  );

-- Admins can view any user
CREATE POLICY "Admins can view users"
  ON users
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid() AND user_roles.role_id = 1
    )
  );

-- Admins can update any user
CREATE POLICY "Admins can update users"
  ON users
  FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid() AND user_roles.role_id = 1
    )
  );

-- Admins can insert any user
CREATE POLICY "Admins can insert users"
  ON users
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid() AND user_roles.role_id = 1
    )
  );

-- Admins can delete any user
CREATE POLICY "Admins can delete users"
  ON users
  FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid() AND user_roles.role_id = 1
    )
  );