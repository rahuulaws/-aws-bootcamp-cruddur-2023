-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Andrew Bayko','bayko@exampro.co' , 'bayko' ,'MOCK'),
  ('Amazon','rahuulshinde+10@gmail.com' , 'AWS' ,'4979bf8b-4fa1-4139-98e3-e4621a37202d'),
  ('R01','rahuulshinde@gmail.com' , 'Rahuul' ,'a276d01d-c6de-4c32-8a47-422fd2a0c7ab'),
  ('RA5','rahuulshinde+5@gmail.com' , 'rahuuls' ,'b1e9be44-0cb2-4b3d-aa93-90f33d9044fc'),
  ('Londo Mollari','lmollari@centari.com' ,'londo' ,'MOCK');
 

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'rahuuls' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  );