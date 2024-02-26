# Emails

- use react-email package.

### Installation

- `npm i react-email @react-email/components`
- in your package.json you can add a script that react-email provides to preview emails:
  - Use a port other than 3000(default) so you don't conflict with your react app if needed with the -p flag

```json
  "scripts": {
    //...,
    "preview-email": "email dev -p 3030"
  },
```

- NOTE: before running the preview email command add the generated files to gitignore: `.react-email/`
  - when running the preview command it will give you a link with a port to open in the browser to view the emails

### Email templates

- Create a new root folder called `emails` (same level as `app/`)
- create tsx files for the template
  Example:

```javascript
import React from "react";
import {
  Html,
  Body,
  Container,
  Text,
  Link,
  Preview,
} from "@react-email/components";

const WelcomeTemplate = ({ name }: { name: string }) => {
  return (
    <Html>
      <Preview>Welcome</Preview>
      <Body>
        {/* Container centers the content */}
        <Container>
          <Text>Hello {name}</Text>
          <Link href="https://google.com">Google</Link>
        </Container>
      </Body>
    </Html>
  );
};

export default WelcomeTemplate;
```

### Styling emails

- use css properties or tailwind

#### CSS

- just use the style property on the components:

```javascript
<Text style={heading}>email text</Text>;
// ...
const body: CSSProperties = {
  background: "#fff",
};
const heading: CSSProperties = {
  fontSize: 32,
};
```

#### Tailwind

- import Tailwind from react-email/components
- wrap the components you want to use Tailwind on

```javascript
<Tailwind>
  <Body style={body}>
    {/* Container centers the content */}
    <Container>
      <Text className="font-bold text-3xl">Hello {name}</Text>
      <Link href="https://google.com">Google</Link>
    </Container>
  </Body>
</Tailwind>
```

### Sending emails

- react-email integrates with [various services](https://react.email/docs/introduction#integrations)
- Resend is made by the same team as React-email
  - free for up to 3000 emails
- signup for Resend and add an api key (copy it to .env)
- install resend: `npm i resend@1.0.0`
- Note: sending emails should be part of your business operations (i.e. when someone submits an order, then you send an email)
  - we create a dummy endpoint in this app for demo purposes.
- add a domain in resend to authorize sending from a domain you own at https://resend.com/domains

```javascript
import WelcomeTemplate from "@/emails/WelcomeTemplate";
import { NextResponse } from "next/server";
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST() {
  await resend.emails.send({
    // from has to be a domain that you own (i.e. gmail, yahoo etc.)
    // configure the domain at https://resend.com/domains - add a dns record so resend knows you're authorized to send emails from that domain
    from: "mydomainemail@gmail.com",
    to: "someemail@gmail.com",
    subject: "some subject",
    // reqact component that represents the email template
    react: <WelcomeTemplate name="Customer Name" />,
  });

  return NextResponse.json({});
}
```
