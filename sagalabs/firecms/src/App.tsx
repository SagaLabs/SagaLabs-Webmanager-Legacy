import { useCallback } from "react";
import { useDataEnhancementPlugin } from "@firecms/data_enhancement";
import { User as FirebaseUser } from "firebase/auth";
import { Authenticator, FirebaseCMSApp } from "firecms";
import "typeface-rubik";
import "@fontsource/ibm-plex-mono";
import { firebaseConfig } from "./firebase-config.ts";
import { rangesCollection } from "./collections/ranges.tsx";
import { docsCollection } from "./collections/docs.tsx";
import { usersCollection } from "./collections/users.tsx"; // Import the usersCollection
import { BrowserRouter } from "react-router-dom";

export default function App() {
  const myAuthenticator: Authenticator<FirebaseUser> = useCallback(
    async ({ user, authController }) => {
      if (user?.email?.includes("flanders")) {
        throw Error("Stupid Flanders!");
      }

      console.log("Allowing access to", user?.email);
      const sampleUserRoles = await Promise.resolve(["admin"]);
      authController.setExtra(sampleUserRoles);

      return true;
    },
    []
  );

  const dataEnhancementPlugin: any = useDataEnhancementPlugin({
    getConfigForPath: ({ path }) => {
      return true;
    },
  });

  return (
    <FirebaseCMSApp
      name={"SagaLabs CMS"}
      basePath={"/firecms"}
      plugins={[dataEnhancementPlugin]}
      authentication={myAuthenticator}
      collections={[rangesCollection, docsCollection, usersCollection]} // Add usersCollection here
      firebaseConfig={firebaseConfig}
    />
  );
}
