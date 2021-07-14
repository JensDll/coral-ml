using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts
{
    public static class StoredProcedures
    {
        public static class Record
        {
            private const string Prefix = "spRecord_";

            public const string GetWithRecordTypeId = Prefix + "GetWithRecordTypeId";

            public const string GetById = Prefix + "GetById";

            public const string GetLoaded = Prefix + "GetLoaded";

            public const string Download = Prefix + "Download";

            public const string Create = Prefix + "Create";

            public const string SetLoaded = Prefix + "SetLoaded";

            public const string Delete = Prefix + "Delete";
        }

        public static class RecordType
        {
            private const string Prefix = "spRecordType_";

            public const string GetAll = Prefix + "GetAll";
        }
    }
}
