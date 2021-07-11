using Application.Data.Models;
using Contracts.Response;
using Domain.DataTransfer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Mapping.Model
{
    public interface ITFLiteRecordResponseMapper
    {
        EnumerableEnvelope<TFLiteRecordGetAllDto>
            MapGetAllResponse(EnumerableEnvelope<TFLiteRecordModel> envelope);
    }
}
