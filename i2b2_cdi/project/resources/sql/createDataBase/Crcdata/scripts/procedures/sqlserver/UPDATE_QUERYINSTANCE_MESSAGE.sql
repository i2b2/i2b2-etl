--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
create procedure UPDATE_QUERYINSTANCE_MESSAGE (@message  varchar(MAX), @instanceId int , @errorMsg varchar(MAX) = NULL OUTPUT) as 
begin 

BEGIN TRY
BEGIN TRANSACTION

update qt_query_instance set message = @message where query_instance_id = @instanceId

 COMMIT
 END TRY 
 BEGIN CATCH
   if @@TRANCOUNT > 0 
      ROLLBACK
   declare @errMsg nvarchar(MAX), @errSeverity int
   select @errMsg = ERROR_MESSAGE(), @errSeverity = ERROR_SEVERITY()
   set @errorMsg = @errMsg
   RAISERROR(@errMsg,@errSeverity,1)
 END CATCH
end