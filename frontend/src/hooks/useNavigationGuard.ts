import { useBlocker } from "react-router-dom";
import { useState, useEffect } from "react";

export const useNavigationGuard = (shouldBlock: boolean) => {
  const [showDialog, setShowDialog] = useState(false);
  const [tx, setTx] = useState<any>(null);

  const blocker = useBlocker(shouldBlock);

  useEffect(() => {
    if (blocker.state === "blocked") {
      setTx(blocker);
      setShowDialog(true);
    }
  }, [blocker]);

  const confirmNavigation = () => {
    tx?.proceed(); // ✅ allow navigation
    setShowDialog(false);
  };

  const cancelNavigation = () => {
    tx?.reset(); // ✅ cancel navigation
    setShowDialog(false);
  };

  return { showDialog, confirmNavigation, cancelNavigation };
};
