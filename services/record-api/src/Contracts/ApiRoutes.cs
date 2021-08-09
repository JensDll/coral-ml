using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts
{
    public static class ApiRoutes
    {
        private const string Base = "api";

        public static class Record
        {
            public const string GetWithRecordTypeId = Base + "/record/type/{recordTypeId}";

            public const string GetLoaded = Base + "/record/loaded";

            public const string GetById = Base + "/record/{id}";

            public const string Download = Base + "/record/download/{id}";

            public const string Upload = Base + "/record";

            public const string SetLoaded = Base + "/record/loaded/{id}";

            public const string Unload = Base + "/record/unload";

            public const string Delete = Base + "/record/{id}";
        }

        public static class RecordType
        {
            public const string GetAll = Base + "/recordType";
        }
    }
}
